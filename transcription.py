import whisper
import os
import shutil
from operation_fichier import extract_audio_fmp4
from operation_fichier import file_size_Mo, file_size_sec
from operation_fichier import reel_file_format
from operation_fichier import split_audio

modele_dispo = ["base", "small" , "medium" , "turbo"]

def transcription(file_path , mdl):
    """
    Fonction qui retourne la transcription d'un fichier qui contient un audio 
    argements : file_path : chemin du fichier & mdl : modele de moteur de transcription 
    valeur de mdl : [0:3] -->> ["base", "small" , "medium" , "turbo"]
    """
    # declaration des variable a utiliser pendant le traitement
    useSplit = False
    useExtract = False
    fileNb = 0
    outDir = ""
    temp_file_name = ""

    #on verifie si le fichier est au format mp4 c'est le cas on extrait l'audio pour alleger le fichier
    if(reel_file_format(file_path) == "mp4"):
        temp_file_name = file_path
        temp = extract_audio_fmp4(file_path)
        file_path = os.path.join(os.getcwd(), temp)
        useExtract = True
    
    #verification des conditions optimale pour faire tourner whisper 
    # - fichier < 25Mo  || < 10min
    if(file_size_Mo(file_path) > 25  or file_size_sec(file_path) > 600):
        fileNb, outDir = split_audio(file_path)
        useSplit = True

    # on charge le modele whisper demander par l'utilisateur au par avant
    modele = whisper.load_model(modele_dispo[mdl])
    
    #deux cas de transcritption 
    #1- on a diviser le fichier originel >> on fait la transcription de chaque fichier disponible dans le dossier
    #2- le fichier n'a pas subit n'a pas etait diviser >> on procede directement a la transcription
    if(useSplit):
        i = 1 #cette indice defiit le numero du fichier a transcrire
        while(i<= fileNb):
            temp_file_path = os.path.join(outDir,f'{i}.mp3')
            transpt = modele.transcribe(temp_file_path)
            yield transpt['text']
            i+=1 
        #destruction du repertoire temporaire qui contient les split
        shutil.rmtree(outDir)
    else :
        transpt = modele.transcribe(file_path)
        yield transpt['text']

    #si on a extrait un audio depuis un fichier mp4 >> on supprime le fichier extrait 
    if(useExtract):
            os.remove(file_path)
            file_path = temp_file_name
    
print(list(transcription("./fichierTeste/3.mp3",0)))
