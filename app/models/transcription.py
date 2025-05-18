import whisper
import os
import shutil
import torch
import json
from app.models.operation_fichier import (
    extract_audio_fmp4,
    file_size_Mo,
    file_size_sec,
    reel_file_format,
    split_audio
)

modele_dispo = ["base", "small", "medium", "turbo"]



def custom_tokenize(text):
    # =============================================================================
    # Auteur  : HAMMOUCHE Anis
    # Email   : anis.hammouche@etu.u-paris.fr
    # Version : 1.0
    # =============================================================================
    """
    Tokenise un texte en séparant par espaces, puis combine les tokens qui sont issus
    d'une division par apostrophe. Par exemple, "m'appeler" sera reconstruit en un seul token.

    Arguments:
        text (str): Le texte à tokeniser.

    Retourne:
        list: La liste des tokens.
    """
    tokens = text.split()
    combined_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Si le token suivant existe et commence par une apostrophe, on combine.
        if i + 1 < len(tokens) and tokens[i + 1].startswith("'"):
            combined_tokens.append(token + tokens[i + 1])
            i += 2
        else:
            combined_tokens.append(token)
            i += 1
    return combined_tokens


def extraire_mapping_depuis_segments(combined_segments):
    # =============================================================================
    # Auteur  : HAMMOUCHE Anis
    # Email   : anis.hammouche@etu.u-paris.fr
    # Version : 1.0
    # =============================================================================
    """
    Combine les segments en un seul texte global et crée un mapping mot par mot.
    Dans chaque segment, si des word-level timestamps sont fournis, on combine les tokens
    qui correspondent à une division par apostrophe (ex : "m" et "'appeler" deviennent "m'appeler").

    Arguments :
        combined_segments (list): Liste de dictionnaires, chacun avec :
            - "start": float, temps de début du segment
            - "end": float, temps de fin du segment
            - "text": str, texte du segment
            - "word_timestamps" (optionnel): liste de dictionnaires avec clés "start", "end", "word"

    Retourne :
        tuple: (texte_global, mapping_data)
            texte_global (str): Le texte complet combiné.
            mapping_data (list): Liste de tuples (start_time, end_time, start_idx, end_idx) pour chaque mot.
    """
    texte_global = ""
    mapping_data = []
    current_index = 0  # Indice dans le texte global
    last_word_end = 0.0  # Dernier timestamp de fin traité

    for seg in combined_segments:
        seg_text = seg.get("text", "").strip()
        seg_start = seg.get("start", 0.0)
        seg_end = seg.get("end", 0.0)

        # Réajuster le début du segment pour éviter les chevauchements
        adjusted_start = max(seg_start, last_word_end)

        if seg.get("word_timestamps"):
            # Combine les tokens si nécessaire : on crée une nouvelle liste de timestamps combinés.
            combined_word_ts = []
            word_ts = seg["word_timestamps"]
            i = 0
            while i < len(word_ts):
                token = word_ts[i]
                word = token.get("word", "").strip()
                # Si le prochain token commence par une apostrophe, on combine
                if i + 1 < len(word_ts) and word_ts[i + 1].get("word", "").startswith("'"):
                    next_token = word_ts[i + 1]
                    combined_word = word + next_token.get("word", "")
                    combined_token = {
                        "word": combined_word,
                        "start": token.get("start", 0.0),
                        "end": next_token.get("end", 0.0)
                    }
                    combined_word_ts.append(combined_token)
                    i += 2
                else:
                    combined_word_ts.append(token)
                    i += 1

            # Utiliser les timestamps combinés
            for token in combined_word_ts:
                word = token.get("word", "").strip()
                # Calcul du temps absolu en utilisant l'offset du segment
                word_start = adjusted_start + (token.get("start", 0.0) - seg_start)
                word_end = adjusted_start + (token.get("end", 0.0) - seg_start)
                word_start = max(word_start, last_word_end)
                mapping_data.append((word_start, word_end, current_index, current_index + len(word)))
                texte_global += word + " "
                current_index += len(word) + 1
                last_word_end = word_end
        else:
            # Si aucun timestamp par mot n'est fourni, on divise uniformément le segment
            words = custom_tokenize(seg_text)
            duration = seg_end - adjusted_start
            word_count = len(words)
            word_duration = duration / word_count if word_count > 0 else 0
            for i, word in enumerate(words):
                word_start = adjusted_start + word_duration * i
                word_end = word_start + word_duration
                word_start = max(word_start, last_word_end)
                mapping_data.append((word_start, word_end, current_index, current_index + len(word)))
                texte_global += word + " "
                current_index += len(word) + 1
                last_word_end = word_end

    return texte_global.strip(), mapping_data


def ajuster_mapping(ancien_text, nouveau_text, ancien_mapping):
    # =============================================================================
    # Auteur  : HAMMOUCHE Anis
    # Email   : anis.hammouche@etu.u-paris.fr
    # Version : 1.0
    # =============================================================================
    """
    Ajuste le mapping des timestamps en fonction du nouveau texte.

    Arguments:
        ancien_text (str): Le texte original.
        nouveau_text (str): Le texte modifié.
        ancien_mapping (list of tuples): Ancien mapping sous la forme
                                         [(start_time, end_time, start_idx, end_idx), ...].

    Retourne:
        list of tuples: Nouveau mapping recalculé.
    """
    new_tokens = custom_tokenize(nouveau_text)
    old_tokens = custom_tokenize(ancien_text)

    # Cas 1 : Nombre de tokens inchangé -> ajustement direct
    if len(new_tokens) == len(old_tokens):
        new_mapping = []
        current_index = 0
        for i, token in enumerate(new_tokens):
            start_time, end_time, _, _ = ancien_mapping[i]
            new_start = current_index
            new_end = new_start + len(token)
            new_mapping.append((start_time, end_time, new_start, new_end))
            current_index = new_end + 1
        return new_mapping

    # Cas 2 : Ajout/Suppression de mots → Adapter le mapping
    new_mapping = []
    ancien_start_time = ancien_mapping[0][0]
    ancien_end_time = ancien_mapping[-1][1]
    total_duration = ancien_end_time - ancien_start_time

    # Méthode 1 : Si le changement est mineur (±15% des tokens), on ajuste progressivement
    if 0.85 * len(old_tokens) <= len(new_tokens) <= 1.15 * len(old_tokens):
        min_len = min(len(old_tokens), len(new_tokens))
        current_index = 0
        for i in range(min_len):
            start_time, end_time, _, _ = ancien_mapping[i]
            token = new_tokens[i]
            new_start_idx = current_index
            new_end_idx = new_start_idx + len(token)
            new_mapping.append((start_time, end_time, new_start_idx, new_end_idx))
            current_index = new_end_idx + 1

        # Ajout des tokens restants (ajoutés ou supprimés)
        extra_tokens = new_tokens[min_len:]
        extra_time = (ancien_end_time - start_time) / max(1, len(extra_tokens))
        for i, token in enumerate(extra_tokens):
            new_start_time = start_time + i * extra_time
            new_end_time = new_start_time + extra_time
            new_start_idx = current_index
            new_end_idx = new_start_idx + len(token)
            new_mapping.append((new_start_time, new_end_time, new_start_idx, new_end_idx))
            current_index = new_end_idx + 1

        return new_mapping

    # Méthode 2 : Si la modification est trop importante, on répartit uniformément
    word_duration = total_duration / len(new_tokens)
    current_index = 0
    for i, token in enumerate(new_tokens):
        new_start_time = ancien_start_time + word_duration * i
        new_end_time = new_start_time + word_duration
        new_start_idx = current_index
        new_end_idx = new_start_idx + len(token)
        new_mapping.append((new_start_time, new_end_time, new_start_idx, new_end_idx))
        current_index = new_end_idx + 1

    return new_mapping

def get_model():

    with open(os.path.abspath("./assets/JSON/settings.json"), 'r', encoding='utf-8') as fichier:
        settings = json.load(fichier)
    return settings["modelWhisper"]

def transcription(file_path, ):
    # =============================================================================
    # Auteur  : GUIDJOU Danil
    # Email   : danil.guidjou@etu.u-paris.fr
    # Version : 1.0
    # =============================================================================

    """
    Fonction qui retourne un dictionnaire avec le texte complet et le mapping des mots,
    avec les timestamps au niveau des mots.

    Arguments :
        file_path (str): chemin du fichier
        mdl (int): indice du modèle dans ["base", "small", "medium", "turbo"]

    Retourne:
        dict: {"text": texte complet, "mapping": [(start_time, end_time, start_idx, end_idx), ...]}
    """
    useSplit = False
    useExtract = False
    fileNb = 0
    outDir = ""
    temp_file_name = ""
    dc = "cpu"  # par défaut sur CPU

    # Si le fichier est au format mp4, extraire l'audio pour alléger le fichier
    if reel_file_format(file_path) == "mp4":
        temp_file_name = file_path
        temp = extract_audio_fmp4(file_path)
        file_path = os.path.join(os.getcwd(), temp)
        useExtract = True

    # Si le fichier est trop volumineux ( >25Mo ou >10min), le diviser en morceaux
    if file_size_Mo(file_path) > 25 or file_size_sec(file_path) > 600:
        fileNb, outDir = split_audio(file_path)
        useSplit = True

    # Vérifier si un GPU compatible est disponible
    if torch.cuda.is_available():
        dc = "cuda"

    # !! mps n'est pas encore configurer pour les puces M4 faut tester pour les models plus ancien !!
    #elif torch.backends.mps.is_available():
    #   dc = "mps"

    # Charger le modèle Whisper demandé par l'utilisateur
    modele = whisper.load_model(modele_dispo[get_model()], device=dc)

    results = []
    if useSplit:
        for i in range(1, fileNb + 1):
            temp_file_path = os.path.join(os.path.abspath(outDir), f'{i}.mp3')
            transcription_result = modele.transcribe(temp_file_path, word_timestamps=True)  # Activation des word-level timestamps
            results.append(transcription_result)
        shutil.rmtree(outDir)  # Nettoyer les fichiers temporaires
    else:
        transcription_result = modele.transcribe(file_path, word_timestamps=True)  # Activation des word-level timestamps
        results.append(transcription_result)

    # Si on a extrait l'audio d'un fichier mp4, supprimer le fichier temporaire
    if useExtract:
        os.remove(file_path)
        file_path = temp_file_name

    # Combiner tous les segments en un seul tableau
    combined_segments = []
    for res in results:
        for seg in res.get("segments", []):
            combined_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
                "word_timestamps": seg.get("words", [])
            })
    print(results)
    print(combined_segments)
    # Obtenir le texte complet et le mapping des mots
    texte_global, mapping_data = extraire_mapping_depuis_segments(combined_segments)

    return {
        "text": texte_global,
        "mapping": mapping_data,
        "segments": results
    }

# Exemple d'utilisation
if __name__ == "__main__":
   # result = transcription("D:/disc E/vscode pyhton/python/upc projet test/audio.wav", 3)
  #  print(json.dumps(result, ensure_ascii=False, indent=4))
  print(custom_tokenize("bonjour je m'appelle anis. j'ai 25 ans"))
