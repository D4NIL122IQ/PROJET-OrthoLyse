import os
import magic
from pydub import AudioSegment
from pydub.silence import detect_nonsilent, detect_silence


def file_size_Mo(file_path):
    #getsize retourne la taille en octect 
    # 1Mo = 2^20 octet 
    return os.path.getsize(file_path) / pow(2, 20)



def reel_file_format(file_path):
    """"
    Retourne le vrai format d'un fichier
    """
    file_format = magic.Magic(mime=True).from_file(file_path)
    mime_to_format = {
        "audio/mpeg": "mp3",
        "audio/x-wav": "wav",
        "audio/wav": "wav",
        "audio/flac": "flac",
        "audio/ogg": "ogg",
        "video/mp4": "mp4",
    }
    return mime_to_format[file_format]


def file_size_ms(file_path):
    frmt = reel_file_format(file_path)
    return len(AudioSegment.from_file(file_path , format=frmt))

def file_size_sec(file_path):
    #on charge l'audio dans AudioSegment ...
    #puis on obtient la durée en ms -> / 1000 pour l'obtenir en sec
    frmt = reel_file_format(file_path) 
    return ( len(AudioSegment.from_file(file_path , format=frmt)) / 1000)

def extract_audio_fmp4(file_pth):
    """"
    Extration d'un audio d'un fichier mp4
    je prends l'intiative de faire cette extration car un fichier mp3 est moins lourd qu'un fichier mp4 
    -> plus optimiser pour la transcription
    --> ca renvoit le nom du fichier dans le quel est stocker l'audio de cette mp4
    ---> il faut supprimer la convertion a la fin du traitement
    """
    output_name = "convertion.mp3"
    frmt = reel_file_format(file_pth)
    audio = AudioSegment.from_file(file_pth , format=frmt)
    audio.export(output_name, format="mp3")
    return  output_name


#***** ---------------***
# def split_file_size(file_path):
#     """
#     Separtion d'un fichier en plusieurs sous-fichiers de taille inferieurs
#     """
#     output_dir = os.path.join(os.getcwd(), "fileSpliter")
#     print(output_dir)
#     if not os.path.exists(output_dir):
#         os.makedirs("fileSpliter")

#     size = file_size_Mo(file_path)
#     audio
#***** ---------------***
def detect_silnce_inInterval(audio):
    
    # on passe en parametre une segment dans les allentour ou on veut decouper l'audio
    # exemple si je veux decouper un audio chaque 5min -> 3000000ms 
    # donc on chereche le silence entre audio[29900 : 301000] 1s de reflection ou peutetre plus a voir avec les testes
    """
    cette fonction prend comme argument un segment d'un audio et retourne une liste de couple (debut, fin)
    de moment de silence dans le segment passer en parametre
    """
    #detection du silence
    # min_silence_len le temps minimale de silence 
    # silence_thresh le volume en db pour detecter le silence 
    # la durée min du silence est a 900ms et on defini -40db comme le seuil du silence
    # la durée du silence est a configurer par rapport aux tests a venir 
    # plus la durée est longue plus on est sur que la coupure est plus correcte !!! mais et si il ne ya pas de silence aussi long dans tout l'audio ? 
    return detect_silence(audio, min_silence_len=900, silence_thresh=-40)

    


def split_audio(file_path):
    """
    Decouper un fichier en plusieurs sous-fichiers de durée inferieurs a stocker dans le repertoir filleSpliter
    """
    #creation d'un  repertoire temporaire (on le suprime a fin de la transcrption ) pour stocker les fichier génerer
    output_dir = os.path.join(os.getcwd(), "fileSpliter")
    if not os.path.exists(output_dir):
        os.makedirs("fileSpliter")
    
    frmt = reel_file_format(file_path)
    audio = AudioSegment.from_file(file_path, format=frmt)
    
    duration = file_size_ms(file_path)  
    start = 0
    file_number = 1
    while start < duration:
        s1 = min(duration , start+290000) #debut de l'intarvale ou on charche le silence
        s2 = min(duration , start+310000) #fin avec un intervale de 20 seconde
        if(s1 == duration or s2 == duration):
            stop = 0
        else:
            listSilence = detect_silnce_inInterval(audio[s1: s2])
            temp1, temp2 = listSilence[0]
            stop = ((temp1+temp2)//2)
        end = min(duration , start+290000+ stop) #on decoupe l'audio en morceau de 5min -> 300sec -> 30000ms
        segement = audio[start:end]
        #enregitrement dans le repertoir fileSpliter
        file_dir = os.path.join(output_dir,f'{file_number}.mp3')
        print(file_dir)
        segement.export(file_dir, format=reel_file_format(file_path))
        start = end #actualiser le debut pour la prochaine decoupe || fin de decoup 
                    # note a danil et si on ajoute 1ms pour que ze3ma ca fait 0-1000ms puis 1001ms-2001ms a tester
        file_number +=1
    
    #on retourne le nbr de fichier pour pouvoir les parcourir afin de faire de la transcription
    return file_number, output_dir
