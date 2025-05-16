import sys
import os
import json
from pydub import AudioSegment
from pydub.silence import detect_silence

def find_ffmpeg():
    """Détecte le chemin de FFmpeg pour PyDub"""
    if getattr(sys, 'frozen', False):
        # En mode bundle PyInstaller
        base_path = sys._MEIPASS
        ffmpeg_path = os.path.abspath(os.path.join(base_path, '_internal', 'ffmpeg'))
    else:
        # En mode développement
        ffmpeg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../bin', 'ffmpeg'))
    return ffmpeg_path

AudioSegment.converter = find_ffmpeg()

def file_size_ms(file_path):
    """Retourne la durée du fichier audio en millisecondes"""
    format = os.path.splitext(file_path)[1].lstrip(".")
    audio = AudioSegment.from_file(file_path, format=format)
    return len(audio)

def file_size_sec(file_path):
    """Retourne la durée du fichier audio en secondes"""
    return file_size_ms(file_path) / 1000

def extract_audio(file_path):
    """Extrait l'audio d'un fichier MP4 et l'exporte en MP3"""
    output_name = "conversion.mp3"
    format = os.path.splitext(file_path)[1].lstrip(".")
    audio = AudioSegment.from_file(file_path, format=format)
    audio.export(output_name, format="mp3")
    return output_name

def split_audio(file_path):
    """Découpe un fichier audio en plusieurs segments et les sauvegarde"""
    output_dir = os.path.join(os.getcwd(), "fileSpliter")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    format = os.path.splitext(file_path)[1].lstrip(".")
    audio = AudioSegment.from_file(file_path, format=format)
    duration = file_size_ms(file_path)
    start = 0
    file_number = 0
    result = {}

    while start < duration:
        t1 = 290000  # durée du premier segment
        t2 = 310000  # durée du deuxième segment
        file_number += 1
        listSilence = []
        while not listSilence:
            s1 = min(duration, start + t1)
            s2 = min(duration, start + t2)
            if s1 == duration or s2 == duration:
                stop = 0
                break
            else:
                listSilence = detect_silence(audio[s1:s2], min_silence_len=900, silence_thresh=-40)
                if listSilence:
                    temp1, temp2 = listSilence[0]
                    stop = (temp1 + temp2) // 2
                t2 += 10000  # Augmente l'intervalle si pas de silence détecté

        end = min(duration, start + 290000 + stop)
        segment = audio[start:end]
        file_dir = os.path.join(output_dir, f'{file_number}.mp3')
        segment.export(file_dir, format=format)
        start = end

    result["file_count"] = file_number
    result["output_dir"] = output_dir
    return json.dumps(result)
