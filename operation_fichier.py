import os
from pydub import AudioSegment

def file_size_Mo(file_path):
    #getsize retourne la taille en octect 
    # 1Mo = 2^20 octet 
    return os.path.getsize(file_path) / pow(2, 20)

def file_size_sec(file_path):
    #on charge l'audio dans AudioSegment ...
    #puis on obtient la durée en ms -> / 1000 pour l'obtenir en sec 
    return ( len(AudioSegment.from_file(file_path , format="mp3")) / 1000) 

def file_size_ms(file_path):
    return len(AudioSegment.from_file(file_path , format="mp3"))

    #|| return len(AudioSegment.from_mp3(file_path)) / 1000


#***** ---------------***
# def split_file_size(file_path, file_size=12):
         
#***** ---------------***

def split_file_duration(file_path):
    #creation d'un  repertoire temporaire (on le suprime a fin de la transcrption ) pour stocker les fichier génerer
    output_dir = os.path.join(os.getcwd(), "fileSpliter")
    print(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs("fileSpliter")
    
    audio = AudioSegment.from_file(file_path, format="mp3")
    
    duration = file_size_ms(file_path)  
    print(duration)
    start = 0
    file_number = 1
    while start < duration:
        end = min(duration , start+60000) #on decoupe l'audio en morceau de 5min -> 300sec -> 30000ms
        segement = audio[start:end]
        #enregitrement dans le repertoir fileSpliter
        file_dir = os.path.join(output_dir,f'{file_number}.mp3')
        print(file_dir)
        segement.export(file_dir, format="mp3")
        start = end #actualiser le debut pour la prochaine decoupe || fin de decoup 
                    # note a danil et si on ajoute 1ms pour que ze3ma ca fait 0-1000ms puis 1001ms-2001ms a tester
        file_number +=1

split_file_duration("./fichierTeste/snezy.mp3")