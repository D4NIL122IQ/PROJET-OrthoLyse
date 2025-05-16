# =============================================================================
# Auteur  : GUIDJOU Danil
# Email   : danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
import os
import sys
from pathlib import Path
import subprocess
import json

def find_worker_script():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "audio_worker.py")

def file_size_Mo(file_path):
    """Retourne la taille du fichier en Mo"""
    return os.path.getsize(file_path) / pow(2, 20)

def reel_file_format(file_path):
    """Retourne le vrai format d'un fichier"""
    return Path(file_path).suffix.lstrip(".")

def file_size_ms(file_path):
    """Retroune la durée de l'audio en ms"""
    worker = find_worker_script()
    result = subprocess.run([sys.executable, worker, "file_size_ms", file_path], capture_output=True, text=True)
    return int(result.stdout.strip())

def file_size_sec(file_path):
    """Retourne la duree de l'audio en seconde"""
    return file_size_ms(file_path) / 1000

def extract_audio_fmp4(file_pth):
    """
    Extration d'un audio d'un fichier mp4 via script externe
    Retourne le nom du fichier audio généré (mp3)
    """
    worker = find_worker_script()
    result = subprocess.run([sys.executable, worker, "extract_audio", file_pth], capture_output=True, text=True)
    return result.stdout.strip()

def split_audio(file_path):
    """
    Découper un fichier audio en plusieurs sous-fichiers via script externe
    Retourne le nombre de fichiers et le répertoire de sortie
    """
    worker = find_worker_script()
    result = subprocess.run([sys.executable, worker, "split_audio", file_path], capture_output=True, text=True)
    try:
        output = json.loads(result.stdout.strip())
        return output["file_count"], output["output_dir"]
    except Exception as e:
        print("Erreur split_audio:", e)
        return 0, ""
