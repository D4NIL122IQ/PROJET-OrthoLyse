import whisper
from operation_fichier import split_file_size, file_size_Mo, split_file_duration, file_size_sec

modele_dispo = ["base", "small" , "medium" , "turbo"]

def transcption(model: int, file_pth: str): #chemin absolu vers le fichier
 # dans la docu whisper la taille ideal est de 25mo && la duration ideal est de 10min max mais 25mo ~11-28min
 #pour l'instant je vais utiliser 12Mo ~10min 
    if file_size_Mo(file_pth) > 12 : 
        file = split_file_size(file_pth)
        for f in file:  #note pour le dev a ne pas oublier on retourne le nbr de fichier so on a deja le repertoire ou sont stocker les fichier il suffit de faire une concat
            transcption(model , f)
    elif file_size_sec(file_pth) > 600:
        file = split_file_duration(file_pth)
        for f in file:
            transcption(model,f) #et la genre on delete le repertoir avec os.rmdir(os.path.join(os.getcwd(), "fileSpliter"))
            
    else : 
        modele = whisper.load_model(modele_dispo[model])
        transpt = modele.transcribe(file_pth)
        return transpt["text"]
