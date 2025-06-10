#start
# === Imports standards ===
import os
import sys
import platform
import subprocess
import builtins
builtins.subprocess = subprocess
import re
import json
import time
from collections import defaultdict

_real_perf_counter = time.perf_counter
_last_brint_time = None


# Path to store recent file history next to this script
RECENT_FILES_PATH = os.path.join(os.path.dirname(__file__), "recent_files.json")

def _print_with_time(*args, **kwargs):
    """Print message and show time since last Brint call."""
    global _last_brint_time
    now = _real_perf_counter()
    if _last_brint_time is None:
        print(*args, **kwargs)
    else:
        delta = now - _last_brint_time
        print(f"[+{delta:.3f}s]", *args, **kwargs)
    _last_brint_time = now

import tempfile
import atexit
import ctypes
import threading
import shutil
from datetime import timedelta
import warnings
from functools import partial

from tkinter import Checkbutton
import math



import cProfile
import pstats


# === Imports externes ===
import vlc
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
try:
    import torch
except ImportError:  # pragma: no cover - optional dependency
    torch = None
try:
    import pretty_midi
except ImportError:  # pragma: no cover - optional dependency
    pretty_midi = None
try:
    from basic_pitch.inference import predict
    from basic_pitch import ICASSP_2022_MODEL_PATH
except Exception:  # pragma: no cover - optional dependency
    predict = None
    ICASSP_2022_MODEL_PATH = None
import pygame
import tkinter as tk
from tkinter import filedialog, Frame, Label, Button, Canvas, StringVar, LEFT, X, W
from tkinter import messagebox, simpledialog, Toplevel, Listbox, SINGLE
from pydub import AudioSegment

# --- tempo.py ---
# --- tempo.py optimisé + debug ---
import numpy as np
np.complex = complex  # Pour compatibilité avec librosa

import librosa
import subprocess
import tempfile
import os
import scipy.signal

# import gdrive_uploader
import os
import tempfile



#GDRIVEUPLOADER
import os
# NOUVEAU :
try:
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
except Exception:  # pragma: no cover - optional dependency
    GoogleAuth = None
    GoogleDrive = None



#ZOOMVIDEO

from tkinter import simpledialog, Toplevel, Listbox, Button, Label, SINGLE, Frame

DEBUG_FLAGS = {
    "AUDIO": False,
    "AUTOLOAD": True,
    "AUTOZOOM": False,
    "CHORD": False,
    "CLICK": False,
    "DRAW": False,
    "EDIT": False,
    "EDITOR" : False,
    "ERROR": False,
    "EXPORT": False,
    "GRID": False,
    "HARMONY": False,
    "HIT": False,
    "NHIT": True,
    "JUMP": False,
    "KEYBOARD": False,
    "LOOP": False,
    "MAPPING": False,
    "open_chord_editor_all": False,
    "PHANTOM" : False,
    "PH" : False,
    "PLAYER": False,
    "PRECOMPUTE" : False,
    "RELOAD": True,
    "RESET": True,
    "RHYTHM": False,
    "RLM" : False,
    "SAVE": True,
    "SCORE": False,
    "SEGMENTS": False,
    "SPAM": False,
    "SYNC": False,
    "TBD": False,
    "TEMPO": False,
    "TRACKER": False,
    "WARNING": False,
    "ZOOM": False,
    "BRINT" : False
}

# Minimum allowed zoom window when auto-adjusting after loop marker edits
# Using a 4-second span prevents extremely small or inverted ranges from
# breaking the view during marker inversion.
MIN_ZOOM_RANGE_MS = 4000

import re

def Brint(*args, **kwargs):
    if not args:
        return

    first_arg = str(args[0])
    tags = re.findall(r"\[(.*?)\]", first_arg)

    # 🔒 Mode silencieux global : BRINT = False désactive TOUT
    if DEBUG_FLAGS.get("BRINT", None) is None:
        return

    # 🔒 Mode silencieux global : BRINT = None il fait les filtres
    if DEBUG_FLAGS.get("BRINT", None) is False:
        pass

    # 💥 Mode super-debug : BRINT = True affiche tout
    if DEBUG_FLAGS.get("BRINT", None) is True:
        _print_with_time(*args, **kwargs)
        return

    if not tags:
        # Aucun tag → affichage inconditionnel (si BRINT n'est pas False)
        _print_with_time(*args, **kwargs)
        return

    for tag_str in tags:
        keywords = tag_str.upper().split()
        if any(DEBUG_FLAGS.get(kw, False) for kw in keywords):
            _print_with_time(*args, **kwargs)
            return

    # Sinon → silence

# === CONFIGURATION ===
ROOT_FOLDER_ID = "1nxHMsw2eW6Urf3pLhPB65ZBRL7McHffS"  # Ton dossier Drive principal
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

#debug
DEBUG_MAX_INDEX = 3


# ===== Harmony Utils =====
NOTE_ORDER = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CHROMATIC_SCALE_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CHROMATIC_SCALE_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]



ENHARMONIC_FIX = {
    "Cb": "B",
    "B#": "C",
    "Fb": "E",
    "E#": "F",
}

VALID_NOTES = set(NOTE_ORDER + list(ENHARMONIC_FIX.keys()))

INTERVAL_LABELS = {
    0: "1",    # unisson
    1: "b2",
    2: "2",
    3: "b3",
    4: "3",
    5: "4",
    6: "#4",
    7: "5",
    8: "b6",
    9: "6",
    10: "b7",
    11: "7"
}

DEGREE_COLOR_MAP = {
    "I": "#FF0000",      # rouge
    "ii": "#FF6600",     # vert clair
    "iii": "#FFCC00",    # indigo
    "IV": "#FFFF00",     # orange
    "V": "#33FF66",      # mauve
    "vi": "#00CCFF",     # gris clair
    "vii°": "#0066FF",   # gris foncé
    "?": "#CCCCCC"       # inconnu
}
INTERVAL_COLOR_MAP = {
    0: "#FF0000",  # 1
    1: "#FF3300",  # b2
    2: "#FF6600",  # 2
    3: "#FF9900",  # b3
    4: "#FFCC00",  # 3
    5: "#FFFF00",  # 4
    6: "#99FF00",  # #4
    7: "#33FF66",  # 5
    8: "#00FFCC",  # b6
    9: "#00CCFF",  # 6
    10: "#0066FF", # b7
    11: "#9900FF", # 7
}


MODES = {
    "ionian":      ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
    "dorian":      ["i", "ii", "III", "IV", "V", "vi°", "VII"],
    "phrygian":    ["i", "II", "III", "iv", "V", "VI", "vii°"],
    "lydian":      ["I", "II", "iii", "IV", "V", "vi", "vii°"],
    "mixolydian":  ["I", "ii", "iii", "IV", "v", "vi", "VII"],
    "aeolian":     ["i", "ii°", "III", "iv", "v", "VI", "VII"],
    "locrian":     ["i°", "II", "iii", "iv", "V", "VI", "vii"],
}

ROMAN_TO_SEMITONE = {
    "I": 0, "II": 2, "III": 4, "IV": 5, "V": 7, "VI": 9, "VII": 11,
    "i": 0, "ii": 2, "iii": 4, "iv": 5, "v": 7, "vi": 9, "vii": 11,
    "ii°": 2, "vi°": 9, "vii°": 11, "i°": 0
}

AVAILABLE_MODES = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]

# === RHYTHM SYLLABLE SETS ===
# Each entry maps a rhythm mode to a list of alternative syllable sets.
# Each set contains a name and the sequence of labels for one bar (4 beats).
RHYTHM_SYLLABLE_SETS = {
    "ternary12": [
        {"name": "Triplet", "labels": [
            "1", "T", "L", "2", "T", "L", "3", "T", "L", "4", "T", "L"]},
        {"name": "Shuffled 8ths", "labels": [
            "1", "", "L", "2", "", "L", "3", "", "L", "4", "", "L"]},
        {"name": "Singing eights", "labels": [
            "DA", "BA", "LA", "DA", "BA", "LA", "DA", "BA", "LA",
            "DA", "BA", "LA"]},
        {"name": "Rapid Valse", "labels": [
            "1", "2", "3", "2", "2", "3", "3", "2", "3", "4", "2", "3"]},
    ],
    "ternary24": [
        {"name": "Split Triplet", "labels": [
            "1", "n", "T", "n", "L", "n", "2", "n", "T", "n", "L", "n",
            "3", "n", "T", "n", "L", "n", "4", "n", "T", "n", "L", "n"]},
        {"name": "Shuffled 16ths", "labels": [
            "1", "", "y", "n", "", "a", "2", "", "y", "n", "", "a",
            "3", "y", "", "n", "", "a", "4", "", "y", "n", "", "a"]},
        {"name": "Split Valse", "labels": [
            "1", "n", "2", "n", "3", "n", "2", "n", "2", "n", "3", "n",
            "3", "n", "2", "n", "3", "n", "4", "n", "2", "n", "3", "n"]},
    ],
    "ternary36": [
        {"name": "Nonets", "labels": [
            "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "2", "2", "3", "4", "5", "6", "7", "8", "9",
            "3", "2", "3", "4", "5", "6", "7", "8", "9",
            "4", "2", "3", "4", "5", "6", "7", "8", "9",]},
    ],
    "binary4": [
        {"name": "4ths", "labels": ["1", "2", "3", "4"]},
    ],
    "binary8": [
        {"name": "Straight 8ths", "labels": ["1", "&", "2", "&", "3", "&", "4", "&"]},
    ],
    "binary16": [
        {"name": "Straight 16ths", "labels": [
            "1", "y", "n", "a", "2", "y", "n", "a",
            "3", "y", "n", "a", "4", "y", "n", "a"]},
    ],
}

# Mapping from internal subdivision modes to the syllable set keys
MODE_TO_SYLLABLE_KEY = {
    "binary8": "binary8",
    "binary16": "binary16",
    "binary4": "binary4",
    "ternary12": "ternary12",
    "ternary24": "ternary24",
    "ternary36": "ternary36",
    "ternary8": "ternary12",
    "ternary16": "ternary24",
}

# Order for cycling through all subdivision modes
ALL_SUBDIVISION_MODES = [
    "binary4",
    "binary8",
    "binary16",
    "ternary12",
    "ternary24",
    "ternary36",
]

def extract_tonic_from_chord(chord_name):
    """
    Extrait la tonique d’un nom d’accord (ex : 'Dm7b5' → 'D', 'Abmaj7' → 'Ab').
    """
    import re
    if not chord_name:
        return "?"
    match = re.match(r"^([A-Ga-g][#b]?)([^A-G]*)", chord_name.strip())
    if match:
        return match.group(1).upper()
    return "?"



def normalize_note_entry(raw_note, key="C", mode="ionian"):
    """
    Nettoie une note entrée par l'utilisateur (min/maj, chiffre, etc.)
    - Convertit '5' en note de la key/mode
    - Corrige les enharmoniques
    - Rejette les trucs type 'Am' ou 'v'
    """
    note = raw_note.strip().upper()

    if not note:
        return None

    # Si c’est un degré ("5" → "G" dans C ionian)
    if note.isdigit() and 1 <= int(note) <= 7:
        degree_idx = int(note) - 1
        try:
            roman = MODES[mode][degree_idx]
            semitone_offset = ROMAN_TO_SEMITONE[roman]
            base_index = NOTE_ORDER.index(key.upper())
            note_index = (base_index + semitone_offset) % 12
            resolved = NOTE_ORDER[note_index]
            Brint(f"[DEGREE→NOTE] '{note}' → {roman} → {resolved}")
            return resolved
        except Exception as e:
            Brint(f"[DEGREE ERROR] Degré '{note}' invalide → {e}")
            return None

    # Corriger enharmoniques (Fb, B#...)
    if note in ENHARMONIC_FIX:
        note = ENHARMONIC_FIX[note]

    # Valider note finale
    if note not in VALID_NOTES:
        Brint(f"[NOTE CLEAN] ❌ Note invalide : '{raw_note}' → ignorée")
        return None

    return note
    
    
def get_interval_from_note(note, key):
    """
    Retourne (intervalle 0–11, label type '3', 'b7', etc.)
    pour une note donnée dans une tonalité de référence (key).
    """

    NOTE_ALIASES = {
        "B#": "C",  "E#": "F",  "CB": "B",  "FB": "E",
        "DB": "C#", "EB": "D#", "GB": "F#", "AB": "G#", "BB": "A#",
        "A#": "Bb", "C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab"
    }

    def extract_key_root(key_raw):
        key_raw = key_raw.strip()
        match = re.match(r"^([A-Ga-g])([b#]?)(.*)", key_raw)
        if not match:
            return None  # non reconnu
        note_base = match.group(1).upper()
        accidental = match.group(2)
        return NOTE_ALIASES.get(note_base + accidental, note_base + accidental)

    Brint(f"[DEBUG EDITOR CHECK] Raw input → note='{note}', key='{key}'")

    note = note.strip().upper()
    note = NOTE_ALIASES.get(note, note)

    key_base = extract_key_root(key)
    Brint(f"[DEBUG EDITOR CHECK] Cleaned → note='{note}', key='{key_base}'")

    if note not in NOTE_ORDER or key_base not in NOTE_ORDER:
        Brint(f"[EDITOR INTERVAL ERROR] note={note} or key={key_base} not in chromatic scale")
        return None, "?"

    note_index = NOTE_ORDER.index(note)
    key_index = NOTE_ORDER.index(key_base)
    interval = (note_index - key_index) % 12
    label = INTERVAL_LABELS.get(interval, "?")

    Brint(f"[EDITOR INTERVAL DEBUG] {note} par rapport à {key_base} → intervalle {interval} ({label})")

    return interval, label
    

def get_interval_from_chord(note, chord_root):
    note_name, _ = normalize_note(note)
    root_name, _ = normalize_note(chord_root)

    i_note = NOTE_ORDER.index(note_name)
    i_root = NOTE_ORDER.index(root_name)

    interval = (i_note - i_root) % 12
    return INTERVAL_LABELS[interval]

def get_interval_from_key(note, key):
    note_name, _ = normalize_note(note)
    key_name, _ = normalize_note(key + "4")  # force octave factice

    i_note = NOTE_ORDER.index(note_name)
    i_key = NOTE_ORDER.index(key_name)

    interval = (i_note - i_key) % 12
    return INTERVAL_LABELS[interval]

def normalize_note(note):
    """Simplifie Bb → A#, etc. et isole nom + octave"""
    note = note.upper().replace("♭", "b").replace("♯", "#")
    if note.endswith("M") or note.endswith("m"):
        note = note[:-1]  # enlève les suffixes accidentels
    if len(note) == 3:
        return note[:2], int(note[2])  # ex: C#4
    else:
        return note[0], int(note[1])   # ex: C4



def normalize_chord_name(chord_name_raw):
    """Normalise un nom d'accord en respectant la casse standard : 
    - Première lettre majuscule (fondamentale)
    - Suffixe laissé tel quel (m, 7, dim...)
    """
    chord_name_raw = chord_name_raw.strip()
    if not chord_name_raw:
        return ""
    return chord_name_raw[0].upper() + chord_name_raw[1:]


def recalculate_chord_for_new_key(chord_name, previous_key, new_key, mode): 
    """
    Recalcule un accord en changeant de clé et en respectant le mode.
    """
    Brint(f"\n[RECALC] Début recalcul {chord_name} : de {previous_key} ➔ {new_key} | mode {mode}")

    if not chord_name or not previous_key or not new_key:
        Brint(f"[WARNING] ➡ Données incomplètes ➔ {chord_name} conservé")
        return chord_name

    # Étape 1 : trouver le degré de l'accord dans l'ancienne key
    deg_old_key = degree_from_chord(chord_name, previous_key, mode)
    Brint(f"[DEBUG] ➡ Étape 1 : {chord_name} ➔ degré {deg_old_key} (dans {previous_key})")

    # Étape 2 : extraire le niveau
    level_old = extract_degree_number(deg_old_key)
    if not level_old:
        Brint(f"[WARNING] ➡ Aucun niveau fonctionnel détecté ➔ {chord_name} conservé")
        return chord_name

    # Étape 3 : calculer l'accord diatonique dans la nouvelle clé
    roman_new_key = MODES[mode][level_old - 1]
    chord_new_key = chord_from_degree(roman_new_key, new_key, mode)

    Brint(f"[DEBUG] ➡ Étape 3 : niveau {level_old} ➔ {roman_new_key} ➔ {chord_new_key} (dans {new_key})")
    Brint(f"[RECALC] Fin recalcul : {chord_name} ➔ {chord_new_key}\n")

    return chord_new_key



def recalculate_chord_from_degree(degree_str, new_key, new_mode):
    level = extract_degree_number(degree_str)
    if not level:
        return "?"
    roman = MODES[new_mode][level-1]
    new_chord = enhance_chord_from_degree(roman, chord_from_degree(roman, new_key, new_mode))
    return new_chord


def transpose_chord_absolute(chord, old_key, new_key):
    """Transpose un accord de old_key vers new_key en préservant sa qualité (M, m, 7, etc.)."""
    if not new_key or len(new_key) < 1:
        Brint("[ERROR] Clé vide ou invalide dans transpose_chord_absolute")
        return chord  # On renvoie l'accord sans transposition

    scale = get_chromatic_scale(old_key)
    chord_base = chord[0].upper()
    try:
        chord_index = scale.index(chord_base)
    except ValueError:
        Brint(f"[ERROR] Accord {chord_base} non trouvé dans la gamme {scale}")
        return chord

    scale_new = get_chromatic_scale(new_key)
    try:
        new_chord_base = scale_new[chord_index]
    except IndexError:
        Brint(f"[ERROR] Index {chord_index} hors gamme {scale_new}")
        return chord

    # 🛡 On garde les extensions éventuelles (m, 7, dim, etc.)
    suffix = chord[1:] if len(chord) > 1 else ""
    return new_chord_base + suffix

def extract_degree_number(degree):
    """Extrait le numéro (1-7) d'un degré en chiffres romains ou arabes, peu importe la casse ou les extensions."""
    import re
    if not degree:
        return None
    # Supprimer les extensions, °, m, 7, etc.
    clean_degree = re.sub(r'[^IV1234567]', '', degree.upper())
    # Cas chiffres arabes directs
    if clean_degree.isdigit():
        num = int(clean_degree)
        if 1 <= num <= 7:
            return num
    # Cas chiffres romains
    roman_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
    # Essayer de matcher du plus grand au plus petit
    for r in sorted(roman_map.keys(), key=len, reverse=True):
        if clean_degree.startswith(r):
            return roman_map[r]
    return None


def enhance_chord_from_degree(degree, chord_root):
    result = chord_root

    # Détection diminué et mineur (ordre important !)
    if "°" in degree:
        result += "dim"
    elif degree.islower():
        result += "m"

    # Extensions harmoniques (cumulables)
    if "sus2" in degree:
        result += "sus2"
    if "sus4" in degree:
        result += "sus4"
    if "#5" in degree:
        result += "#5"
    if "7" in degree:
        result += "7"

    return result

def get_chromatic_scale(key):
    if not key:
        Brint("[ERROR] Key is None ou vide dans get_chromatic_scale() ➔ fallback 'C'")
        key = "C"
    if "b" in key:
        return CHROMATIC_SCALE_FLAT
    return CHROMATIC_SCALE_SHARP
def chord_from_degree(degree, key, mode="ionian"):
    if degree not in ROMAN_TO_SEMITONE:
        return "?"
    try:
        root_index = get_chromatic_scale(key).index(key[0].upper())
        scale = get_chromatic_scale(key)
        semitone = (root_index + ROMAN_TO_SEMITONE[degree]) % 12
        chord_root = scale[semitone]
        return chord_root
    except:
        return "?"

def degree_from_chord(chord, key, mode="ionian"):
    if not chord:
        return "?"
    chord_base = chord[0].upper()
    if len(chord) > 1 and chord[1] in ["b", "#"]:
        chord_base += chord[1]

    scale = get_chromatic_scale(key)
    try:
        key_index = scale.index(key[0].upper())
        chord_index = scale.index(chord_base)
    except ValueError:
        return "?"

    semitone_distance = (chord_index - key_index) % 12
    mode_degrees = MODES.get(mode, MODES["ionian"])

    for i, roman in enumerate(mode_degrees):
        expected_semitone = ROMAN_TO_SEMITONE[roman]
        if expected_semitone == semitone_distance:
            degree = roman
            # 🎯 ➡ Analyser la qualité de l'accord et adapter le degré :
            if chord.lower().endswith("dim"):
                # Forcer ° même si le degré diatonique ne l'avait pas
                if "°" not in degree:
                    degree = degree.lower() + "°"
            elif chord.lower().endswith("m"):
                degree = degree.lower()
            # Si l'accord contient 7 et le degré ne l'a pas ➡ on ajoute 7
            if chord.lower().endswith("7") and "7" not in degree:
                degree += "7"
            return degree
    return "?"

def enhance_chord(chord_name, extension=""):
    if not chord_name or chord_name == "?":
        return "?"
    return chord_name + extension


# === AUTHENTICATION ===

def authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    gauth.settings['get_refresh_token'] = True  # 🔁 important pour générer le refresh_token

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # Lancer auth dans le navigateur
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)



# === FOLDER MANAGEMENT ===
def get_or_create_subfolder(parent_folder_id, folder_name, drive):
    """Récupère ou crée un sous-dossier dans Drive"""
    file_list = drive.ListFile({
        'q': f"'{parent_folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and title='{folder_name}'"
    }).GetList()

    if file_list:
        return file_list[0]['id']  # Dossier déjà existant
    else:
        folder_metadata = {
            'title': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': parent_folder_id}]
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

# === LOOP COUNT ===
def count_existing_loops(folder_id, drive):
    """Compte le nombre de loops dans un sous-dossier"""
    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
    }).GetList()
    
    loop_files = [f for f in file_list if f['title'].startswith('loop') and f['title'].endswith('.wav')]
    return len(loop_files)

# === MAIN UPLOAD FUNCTION ===
def upload_loop_to_drive(local_current_path, media_base_name):
    if not os.path.exists(local_current_path):
        Brint(f"[TBD] ❌ Fichier non trouvé : {local_current_path}")
        return

    drive = authenticate()

    # Récupérer ou créer le sous-dossier
    subfolder_id = get_or_create_subfolder(ROOT_FOLDER_ID, media_base_name, drive)

    # Déterminer numéro de loop
    existing_loops = count_existing_loops(subfolder_id, drive)
    next_loop_number = existing_loops + 1
    loop_filename = f"loop{next_loop_number}_{media_base_name}.wav"

    # Upload
    file_drive = drive.CreateFile({
        'title': loop_filename,
        'parents': [{'id': subfolder_id}]
    })
    file_drive.SetContentFile(local_current_path)
    file_drive.Upload()

    Brint(f"[TBD] ✅ Upload terminé : {loop_filename} → Dossier {media_base_name}")






#GDRIVEUPLOADER ENDS

def extract_audio_segment(audio_path, start, duration, sr=22050):
    if os.name == "nt" and audio_path.startswith("/"):
        audio_path = audio_path[1:]  # Corrige le chemin /C:/... en C:/...
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", audio_path,
        "-vn", "-ac", "1", "-ar", str(sr),
        tmp_path
    ]

    Brint("[WARNING] Appel ffmpeg:", " ".join(cmd))
    result = subprocess.run(cmd)
    Brint("[WARNING] Code retour ffmpeg:", result.returncode)

    return tmp_path

def detect_tempo_and_beats(audio_path, loop_start=35.0, loop_end=75.0):
    import time
    start_time_func = time.time() # Renamed start to avoid conflict
    tmp_path = None  # Initialize tmp_path to None
    if os.name == "nt" and audio_path.startswith("/"):
        Brint("[DEBUG] Correction du chemin source audio_path")
        audio_path = audio_path[1:]
    try:
        duration = loop_end - loop_start
        Brint(f"[TBD] === Analyse tempo sur {audio_path} ===")
        Brint(f"[TBD] Loop : {loop_start:.2f}s → {loop_end:.2f}s")

        tmp_path = extract_audio_segment(audio_path, loop_start, duration)
        pass #Brint(f"[DEBUG] Fichier temporaire créé : {tmp_path}")
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            Brint("[TBD] ❌ Fichier audio temporaire vide ou manquant.")
            return None # Ensure to return something identifiable as failure

        y, sr = librosa.load(tmp_path, sr=None, dtype=np.float32)
        if y is None or len(y) == 0:
            Brint("[TBD] ❌ Erreur de chargement audio depuis le fichier WAV.")
            return None # Ensure to return something identifiable as failure
        pass #Brint(f"[DEBUG] Taille fichier : {os.path.getsize(tmp_path)} octets, SR = {sr}, longueur = {len(y)}")

        sos = scipy.signal.butter(4, [40, 120], btype='bandpass', fs=sr, output='sos')
        y_bass = scipy.signal.sosfilt(sos, y)

        frame_length = int(0.05 * sr)
        hop_length = int(0.01 * sr)

        rms_bass = librosa.feature.rms(y=y_bass, frame_length=frame_length, hop_length=hop_length)[0]
        times_bass = librosa.frames_to_time(np.arange(len(rms_bass)), sr=sr, hop_length=hop_length)

        threshold = np.max(rms_bass) * 0.7
        candidates = np.where((rms_bass > threshold) & (times_bass > 1.0))[0]
        if not candidates.size:
            Brint("[TBD] ⚠️ Aucun pic d’énergie clair détecté.")
            return None # Ensure to return something identifiable as failure

        beat1_time = float(loop_start + times_bass[candidates[0]])
        ts = timedelta(seconds=beat1_time)
        hms = f"{ts.seconds // 3600}:{(ts.seconds % 3600) // 60:02}:{ts.seconds % 60:02}.{int(ts.microseconds/1000):03}"
        Brint(f"[TBD] 🌟 Beat 1 : {hms} ({beat1_time:.3f}s)")

        idx_start_focus = int((beat1_time - loop_start) * sr) # Renamed idx_start to avoid conflict
        y_focus = y[idx_start_focus:idx_start_focus + int(15 * sr)]

        tempo_raw, _ = librosa.beat.beat_track(y=y_focus, sr=sr)
        tempo = float(tempo_raw/3)  # mesure?beat?
        Brint(f"[TBD] 🎵 Tempo beats estimé  : {tempo:.2f} BPM")

        Brint(f"[TIMER] detect_tempo_and_beats: {time.time() - start_time_func:.2f}s")
        return beat1_time, tempo

    except Exception as e:
        # It's better to handle specific cases for returning loop_start/loop_end if needed
        # For a general exception, returning None or raising might be more appropriate
        # The original logic here seems to be a fallback, ensure it's what's intended.
        # For now, replicating the original fallback logic in case of an error,
        # but this might need review depending on how `self` is accessed here.
        # Assuming `self` is not accessible in this global function, returning None.
        Brint(f"[TBD] ❌ Erreur tempo : {type(e).__name__} - {e}")
        return None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

        return self.loop_end / 1000.0 if self.loop_end is not None else None


        return self.loop_start / 1000.0 if self.loop_start is not None else None

        return self.loop_end / 1000.0 if self.loop_end is not None else None

        Brint(f"[TBD] ❌ Erreur tempo : {type(e).__name__} - {e}")





# --- scanfile.py ---
import tkinter as tk
from tkinter import filedialog
import numpy as np
import librosa
import os
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import subprocess
import time

np.complex = complex  # Patch pour compatibilité librosa

SILENCE_THRESHOLD = 0.005
ACTIVE_THRESHOLD = 0.02
FRAME_LENGTH = 1024
HOP_LENGTH = 256


def seconds_to_hms(seconds):
    return str(timedelta(seconds=float(seconds))).split(".")[0]

def format_time(seconds, include_ms=True, include_tenths=False):
    """Format seconds as H:M:S with optional milliseconds or tenths."""
    if seconds is None or seconds < 0:
        if include_ms:
            return "--:--:--.-" if include_tenths else "--:--:--.---"
        return "--:--:--"

    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)

    if include_ms:
        if include_tenths:
            tenths = int((seconds - int(seconds)) * 10)
            return f"{h}:{m:02}:{s:02}.{tenths}"
        ms = int(round((seconds - int(seconds)) * 1000))
        return f"{h}:{m:02}:{s:02}.{ms:03}"
    return f"{h}:{m:02}:{s:02}"

def _util_extract_audio_segment(
    input_path,
    output_path=None,
    *,
    start_sec=None,
    duration_sec=None,
    audio_codec="pcm_s16le",
    sample_rate=44100,
    channels=1,
    overwrite=True,
    use_temp_file=True,
):
    """Extract an audio segment via ffmpeg."""
    if output_path is None:
        if use_temp_file:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                output_path = tmp.name
        else:
            raise ValueError("output_path required if use_temp_file=False")

    cmd = ["ffmpeg"]
    if overwrite:
        cmd.append("-y")
    if start_sec is not None:
        cmd += ["-ss", str(start_sec)]
    if duration_sec is not None:
        cmd += ["-t", str(duration_sec)]
    cmd += ["-i", input_path, "-vn", "-acodec", audio_codec, "-ar", str(sample_rate), "-ac", str(channels), output_path]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        return None

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        return None

    return output_path

def _util_get_tempo_and_beats_librosa(y, sr):
    """Return tempo and beat frames from audio using librosa."""
    if y is None or len(y) == 0:
        return 0.0, np.array([])
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        return float(tempo), beats
    except Exception:
        return 0.0, np.array([])

def extract_keyframes(
    video_path,
    start_time_sec=None,
    duration_sec=None,
    end_time_sec=None,
):
    """Extract keyframe timestamps from a video using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "frame=pkt_pts_time,pict_type",
        "-of",
        "csv=p=0",
        video_path,
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode()
    except Exception:
        return []
    keyframes = []
    for line in output.strip().splitlines():
        try:
            time_str, frame_type = line.split(",")
        except ValueError:
            continue
        if frame_type.strip() == "I":
            try:
                t = float(time_str)
            except ValueError:
                continue
            keyframes.append(t)

    if start_time_sec is not None:
        end = start_time_sec + duration_sec if duration_sec is not None else end_time_sec
        if end is not None:
            keyframes = [t for t in keyframes if start_time_sec <= t < end]
        else:
            keyframes = [t for t in keyframes if t >= start_time_sec]

    return keyframes

def detect_countins_with_rms(filepath, hop_length=256, strict=False, mode="default", verbose=True):
    threshold = 0.01 if strict else 0.03
    lin_threshold = 0.05
    y, sr = librosa.load(filepath, sr=None, mono=True)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr, hop_length=hop_length)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop_length)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    peaks, _ = find_peaks(onset_env, height=0.2 * np.max(onset_env), distance=int(0.4 * sr / hop_length))
    click_times = onset_times[peaks]



    def rms_mean_between(start, end):
        mask = (rms_times >= start) & (rms_times <= end)
        return np.mean(rms[mask]) if np.any(mask) else 0

    def is_stable_plateau(start, end):
        mask = (rms_times >= start) & (rms_times <= end)
        segment = rms[mask]
        if len(segment) <= 5:
            return False, {
                "reason": "segment_too_short",
                "mean_rms": None,
                "std_rms": None,
                "mean_ok": False,
                "std_ok": False
            }

        mean_rms = np.mean(segment)
        std_rms = np.std(segment)
        mean_ok = mean_rms > 0.008
        std_ok = std_rms < 0.025

        return (mean_ok and std_ok), {
            "mean_rms": round(float(mean_rms), 6),
            "std_rms": round(float(std_rms), 6),
            "mean_ok": mean_ok,
            "std_ok": std_ok
        }

    groups = []
    if verbose:
        Brint(f"\n⏺️ Tous les click_times : {[round(float(t), 3) for t in click_times]}")
    for i in range(len(click_times) - 3):
        for j in range(i + 3, min(i + 6, len(click_times) + 1)):
            group = click_times[i:j]
            intervals = np.diff(group)
            if len(intervals) < 2:
                continue
            avg = np.mean(intervals)
            std = np.std(intervals)
            max_dev = np.max(np.abs(intervals - avg))
            beat1 = group[0] + 4 * avg
            rms_before = rms_mean_between(group[0] - 1.0, group[0])
            rms_after = rms_mean_between(beat1, beat1 + 1.0)
            plateau_ok, plateau_debug = is_stable_plateau(beat1, beat1 + 1.0)

            boost = rms_after / rms_before if rms_before > 0 else float("inf")

            clicks_sec = [round(float(t), 3) for t in group]
            clicks_hms = [seconds_to_hms(t) for t in group]

            if verbose:
                Brint(f"[TBD]   → Clics candidats : {clicks_hms} | Δt = {round(avg, 3)} | STD = {round(std, 4)}")

            if std >= threshold:
                if verbose: Brint(f"[TBD]  {std:.2f}    ❌ Rejeté : irrégulier")
                continue
            if max_dev >= lin_threshold:
                if verbose: Brint(f"[TBD]  {max_dev:.2f}    ❌ Rejeté : déviation max {round(max_dev, 4)} trop élevée")
                continue
            if rms_before > 0.026:
                if verbose: Brint(f"[TBD] {rms_before:.2f}     ❌ Rejeté : pas assez silencieux avant")
                continue
            if boost <= 1.5:
                if verbose: Brint(f"[TBD]  {boost:.2f}    ❌ Rejeté : boost RMS trop faible (×{round(boost,2)})")
                continue
            if not plateau_ok:
                if verbose:
                    Brint(f"[TBD]      ❌ Rejeté : pas de plateau RMS stable")
                    Brint(f"        → Moyenne RMS = {plateau_debug['mean_rms']} (ok={plateau_debug['mean_ok']})")
                    Brint(f"        → Écart-type RMS = {plateau_debug['std_rms']} (ok={plateau_debug['std_ok']})")
                continue

            if verbose: Brint(f"[TBD]      ✅ Accepté comme count-in 🎯")
            groups.append({
                "clicks": clicks_sec,
                "interval": round(float(avg), 3),
                "bpm_ternary": round(60 / (avg * 3), 2),
                "beat1": round(float(beat1), 3),
                "rms_before": round(float(rms_before), 6),
                "rms_after": round(float(rms_after), 6),
                "error": round(float(std), 3)
            })

    # Dédoublonnage
    final_groups = []
    starts_seen = []

    for g in groups:
        start = g["clicks"][0]
        too_close = any(abs(start - s) < 1.0 for s in starts_seen)
        if not too_close:
            final_groups.append(g)
            starts_seen.append(start)

    return final_groups




def open_vlc_at(filepath, seconds):
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    abs_filepath = os.path.abspath(filepath)
    timestamp = int(seconds)

    Brint("[TBD] WARNING", [vlc_path, abs_filepath, f"--start-time={timestamp}"])

    subprocess.run([
        vlc_path,
        abs_filepath,
        f"--start-time={timestamp}"
    ])


    if groups:
        Brint("[TBD] \n🔍 Résultats des count-ins détectés :")
        for i, g in enumerate(groups):
            beat1_hms = seconds_to_hms(g["beat1"])
            start_hms = seconds_to_hms(g["clicks"][0])

            clicks_hms = [seconds_to_hms(t) for t in g["clicks"]]
            boost = round(g["rms_after"] / g["rms_before"], 2) if g["rms_before"] > 0 else "∞"
            Brint(f"[{i+1}] Start @ {start_hms} | BPM: {g['bpm_ternary']} | Intervalle: {g['interval']}s | Clics: {clicks_hms} | RMS boost ×{boost}")

#                Brint(f"[{i+1}] Beat1 @ {beat1_hms} | BPM: {g['bpm_ternary']} | Intervalle: {g['interval']}s | Clics: {clicks_hms} | RMS boost ×{boost}")

        while True:
            choice = input("Taper un numéro pour ouvrir VLC à ce Beat1 (1–5), ou Entrée pour quitter : ").strip()
            if not choice:
                break
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(groups):
                    Brint(f"Ouverture de VLC à {seconds_to_hms(groups[idx]['clicks'][0])}...")
                    open_vlc_at(current_path, groups[idx]["clicks"][0])
                else:
                    Brint("[TBD] Numéro invalide.")
            else:
                Brint("[TBD] Merci d'entrer un numéro valide ou rien pour quitter.")
            
                

        else:
            Brint("[TBD] ❌ Aucun count-in détecté.")
    else:
        Brint("[TBD] ❌ Aucun fichier sélectionné.")


# --- analysis_utils.py ---
import subprocess
import tempfile
import os
import librosa
import numpy as np
import librosa
import numpy as np
import subprocess
import tempfile
import os

import librosa
import numpy as np
import subprocess
import tempfile
import os
try:
    import ffmpeg
except ImportError:  # pragma: no cover - optional dependency
    ffmpeg = None

def detect_multiple_beat1(path, sr=22050, segment_duration=15.0, step=10.0, min_beats=1):
    """
    Analyse tout le fichier en le balayant par fenêtres glissantes,
    et détecte les points d'entrée RHYTHMiques (Beat 1).
    """
    Brint(f"[TBD] 📂 Analyse du fichier : {path}")
    try:
        info = ffmpeg.probe(path)
        duration = float(info['format']['duration'])
    except:
        duration = 600  # fallback

    Brint(f"[TBD] ⏳ Durée totale : {duration:.1f} sec")
    beat1_list = []

    for offset in np.arange(0, duration - segment_duration, step):
        Brint(f"[TBD] \n🔍 Analyse segment {offset:.2f}s → {offset + segment_duration:.2f}s")

        # découpage audio temporaire
        tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp_wav.name
        tmp_wav.close()
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(offset),
            "-t", str(segment_duration),
            "-i", path,
            "-vn",
            "-ac", "1",
            "-ar", str(sr),
            tmp_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            y, sr = librosa.load(tmp_path, sr=sr)
            duration_loaded = len(y) / sr
            Brint(f"[TBD]     ℹ️ Segment chargé : {duration_loaded:.2f}s")

            if len(y) < sr:  # moins de 1s
                Brint("[TBD]     ⚠️ Segment vide ou trop court.")
                continue

            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            if len(beats) >= min_beats:
                beat_times = librosa.frames_to_time(beats, sr=sr)
                beat1_abs = float(beat_times[0] + offset)
                tempo = float(tempo)
                Brint(f"[TBD]     ✅ Beat 1 détecté : {beat1_abs:.2f}s @ {tempo:.1f} BPM")
                beat1_list.append((offset, offset + segment_duration, beat1_abs, tempo))
            else:
                Brint("[TBD]     ❌ Pas assez de beats détectés.")

        except Exception as e:
            Brint(f"[TBD] ⚠️ Erreur analyse : {e}")

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    Brint(f"[TBD] \n🎯 Total Beat 1 détectés : {len(beat1_list)}")
    return beat1_list

def extract_audio_segment(path, offset=0.0, duration=30.0, sr=22050):
    """Découpe propre via ffmpeg pour éviter les problèmes avec librosa + audioread"""
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp_wav.name
    tmp_wav.close()

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(offset),
        "-t", str(duration),
        "-i", path,
        "-vn",
        "-ac", "1",
        "-ar", str(sr),
        tmp_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp_path

def find_beat1_hotspots(path, sr=22050):
    Brint(f"[TBD] \n📂 Analyse globale pour hotspots jamtrack : {path}")

    # 1. Convertir fichier complet en .wav mono via ffmpeg
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp_wav.name
    tmp_wav.close()

    cmd = [
        "ffmpeg", "-y",
        "-i", path,
        "-ac", "1",
        "-ar", str(sr),
        tmp_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        y, sr = librosa.load(tmp_path, sr=sr)
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)

        # 2. Détection des transitions silence → activité
        SILENCE_THRESHOLD = 0.005
        ACTIVE_THRESHOLD = 0.02
        min_silence_duration = 2.0
        min_activity_duration = 6.0

        Brint(f"[TBD] 🎛 Analyse énergie globale : RMS min={rms.min():.4f}, max={rms.max():.4f}, mean={rms.mean():.4f}")
        transitions = []
        i = 0
        while i < len(rms):
            if rms[i] < SILENCE_THRESHOLD:
                silence_start = times[i]
                while i < len(rms) and rms[i] < SILENCE_THRESHOLD:
                    i += 1
                silence_end = times[i] if i < len(rms) else times[-1]

                act_start = i
                while i < len(rms) and rms[i] > ACTIVE_THRESHOLD:
                    i += 1

                # 🛡️ Protection contre dépassement d’index
                if act_start >= len(times) or i >= len(times):
                    continue

                act_end = times[i]
                silence_dur = silence_end - silence_start
                act_dur = act_end - times[act_start]

                if silence_dur >= min_silence_duration and act_dur >= min_activity_duration:
                    transitions.append((silence_end, act_end))
                    Brint(f"[TBD] 🔁 Transition détectée : silence {silence_start:.1f}s → {silence_end:.1f}s, activité jusqu’à {act_end:.1f}s")
            else:
                i += 1

        # 3. Appliquer détection Beat 1 sur chaque zone détectée
        results = []
        for idx, (start, end) in enumerate(transitions):
            Brint(f"[TBD] ⏱️ Zone {idx+1} : {start:.2f}s → {end:.2f}s")
            beat_result = detect_tempo_and_beats(path, loop_start=start, loop_end=end)
            if beat_result:
                beat1, tempo = beat_result
                Brint(f"[TBD]    ✅ Beat 1 : {beat1:.3f}s @ {tempo:.1f} BPM")
                results.append((start, end, beat1, tempo))
            else:
                Brint(f"[TBD]    ❌ Échec détection beat")

        return results

    finally:
        if os.path.exists(tmp_path):
            Brint(f"[TBD] 🧹 Suppression du fichier temporaire : {tmp_path}")
            os.remove(tmp_path)

def detect_jamtrack_zones(path, sr=22050):
    Brint(f"[TBD] \n📂 Fichier à analyser : {path}")
    tmp_path = extract_audio_segment(path, offset=0.0, duration=180.0, sr=sr)
    Brint(f"[TBD] 🎧 Segment audio temporaire généré : {tmp_path}")

    try:
        Brint("[TBD] 🔍 Chargement audio avec librosa...")
        y, sr = librosa.load(tmp_path, sr=sr)
        Brint(f"[TBD] ✅ Chargé : {len(y)} échantillons à {sr} Hz")

        Brint("[TBD] 🎛 Calcul du spectre...")
        S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))**2
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

        Brint("[TBD] 🎚 Extraction bande basse (40–120Hz)...")
        low_band = (freqs >= 40) & (freqs <= 120)
        bass_energy = S[low_band, :].mean(axis=0)
        times = librosa.frames_to_time(np.arange(len(bass_energy)), sr=sr, hop_length=512)

        Brint("[TBD] 📊 Calcul RMS...")
        rms = librosa.feature.rms(y=y).flatten()
        global_threshold = np.percentile(bass_energy, 75)
        Brint(f"[TBD] 📈 Seuil dynamique sur basses : {global_threshold:.4f}")

        Brint("[TBD] 🔍 Détection des frames actives...")
        active = bass_energy > global_threshold
        segments = []
        start = None
        for i, val in enumerate(active):
            if val and start is None:
                start = times[i]
            elif not val and start is not None:
                end = times[i]
                if end - start >= 10.0:
                    segments.append((start, end))
                    Brint(f"[TBD] ⏳ Segment brut détecté : {start:.2f}s → {end:.2f}s")
                start = None

        # Fusionner les segments proches
        merged = []
        for seg in segments:
            if not merged:
                merged.append(seg)
            else:
                last_start, last_end = merged[-1]
                if seg[0] - last_end < 2.0:
                    merged[-1] = (last_start, seg[1])
                else:
                    merged.append(seg)

        Brint(f"[TBD] 🔁 Segments fusionnés : {len(merged)}")
        for i, (start, end) in enumerate(merged):
            Brint(f"[TBD]   ▶ Zone {i+1}: {start:.2f}s → {end:.2f}s")

        # Appliquer détection beat1
        detected = []
        for i, (start, end) in enumerate(merged):
            Brint(f"[TBD] ⏱️ Zone {i+1} : détection tempo sur {start:.2f}s → {end:.2f}s")
            result = detect_tempo_and_beats(path, loop_start=start, loop_end=end)
            if result:
                beat1, tempo = result
                Brint(f"[TBD]     ✅ Beat 1 détecté : {beat1:.3f}s @ {tempo:.2f} BPM")
                detected.append((start, end, beat1))
            else:
                Brint(f"[TBD]     ❌ Échec détection tempo")

        Brint(f"[TBD] \n🎯 Zones retenues : {len(detected)}")
        return detected

    finally:
        if os.path.exists(tmp_path):
            Brint(f"[TBD] 🧹 Suppression du fichier temporaire : {tmp_path}")
            os.remove(tmp_path)


# --- loopmarkersin.py ---
# --- 2_player_step.py corrigé ---
import json
import time
import tkinter as tk
from tkinter import filedialog, Frame, Label, Button, Canvas, StringVar, LEFT, X, W
from tkinter import messagebox
try:
    import psutil
except ImportError:  # pragma: no cover - optional dependency
    psutil = None
from tkinter import simpledialog, Toplevel, Listbox, Button, Label, SINGLE
import vlc
import os

import time
import numpy as np
import librosa
import soundfile as sf
try:
    from basic_pitch.inference import predict
    from basic_pitch import ICASSP_2022_MODEL_PATH
except Exception:  # pragma: no cover - optional dependency
    predict = None
    ICASSP_2022_MODEL_PATH = None
try:
    import pretty_midi
except ImportError:  # pragma: no cover - optional dependency
    pretty_midi = None
import re

try:
    import torch
except ImportError:  # pragma: no cover - optional dependency
    torch = None
import sys
import ctypes
import tempfile
import pygame
dbflag = False

import subprocess

def hms_to_seconds(hms):
    parts = list(map(float, hms.split(":")))
    return sum(t * 60**i for i, t in enumerate(reversed(parts)))


import soundfile as sf

import subprocess
import os
def loopdata_to_dict(loop_data):
    Brint(f"[EXPORT] Préparation de la boucle '{getattr(loop_data, 'name', 'Unnamed')}' pour sauvegarde JSON.")

    loop_dict = {
        "name": getattr(loop_data, "name", "Unnamed"),
        "loop_start": loop_data.loop_start,
        "loop_end": loop_data.loop_end,
        "master_note_list": loop_data.master_note_list if hasattr(loop_data, "master_note_list") else [],
        "chords": loop_data.chords if hasattr(loop_data, "chords") else [],
        "tempo_bpm": getattr(loop_data, "tempo_bpm", None),
        "key": getattr(loop_data, "key", None),
        "loop_zoom_ratio": getattr(loop_data, "loop_zoom_ratio", None),
        "confirmed_hit_context": getattr(loop_data, "confirmed_hit_context", None),
    }

    Brint(f"[OK] Boucle prête : start={loop_dict['loop_start']}, end={loop_dict['loop_end']}, bpm={loop_dict['tempo_bpm']}")
    if loop_dict["tempo_bpm"] is None:
        Brint(f"[WARNING] ❌ tempo_bpm manquant lors de l'export de {loop_dict['name']}")
    else:
        Brint(f"[EXPORT] ✅ tempo_bpm exporté = {loop_dict['tempo_bpm']}")

    return loop_dict


def predict_on_loop_segment(original_path, beat1_sec, duration_sec):
    Brint(f"[TBD] 🎧 Extraction de {duration_sec}s à partir de {beat1_sec}s...")

    # Si le fichier est une vidéo, extraire l'audio en WAV
    if original_path.lower().endswith('.mp4'):
        temp_audio = original_path + ".extracted.wav"
        if not os.path.exists(temp_audio):
            cmd = [
                "ffmpeg",
                "-i", original_path,
                "-vn",  # no video
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "1",
                temp_audio
            ]
            subprocess.run(cmd, check=True)
        audio_path = temp_audio
    else:
        audio_path = original_path

    temp_path = None # Initialize temp_path to None
    try:
        # Charger tout le fichier audio avec soundfile
        y_full, sr = sf.read(audio_path, always_2d=False)

        # Convertir temps en samples
        start_sample = int(beat1_sec * sr)
        end_sample = int((beat1_sec + duration_sec) * sr)

        # Extraction du segment
        y = y_full[start_sample:end_sample]

        # Sauvegarder le segment dans un WAV temporaire
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            temp_path = tmpfile.name
            sf.write(temp_path, y, sr)

        Brint(f"[TBD] 🎧 Analyse de {os.path.basename(temp_path)} (durée {len(y)/sr:.2f}s)")

        # Analyse avec Basic Pitch
        start_predict = time.time()
        model_output, midi_data, note_events = predict(
            temp_path,
            model_or_model_path=ICASSP_2022_MODEL_PATH,
            onset_threshold=0.3,
            frame_threshold=0.3,
            minimum_note_length=30.0,
            minimum_frequency=70.0,
            maximum_frequency=1300.0,
            melodia_trick=True
        )
        Brint(f"[TIMER] Predict: {time.time() - start_predict:.2f}s")

        adjusted_events = [
            (start + beat1_sec, end + beat1_sec, pitch, conf, extra)
            for start, end, pitch, conf, extra in note_events
        ]

        return model_output, midi_data, adjusted_events
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

def export_masked_segment(source_path, dest_path, beat1, duration):
    """
    Crée un fichier audio avec la même longueur que l'original, mais silencieux en dehors de [beat1, beat1+duration]
    """
    y, sr = librosa.load(source_path, sr=None, mono=True)
    total_len = len(y)
    start_sample = int(beat1 * sr)
    end_sample = int((beat1 + duration) * sr)

    y_masked = np.zeros_like(y)
    y_masked[start_sample:end_sample] = y[start_sample:end_sample]
    sf.write(dest_path, y_masked, sr)


def predict_on_interval(filepath, beat1_sec, bpm, measures=20, tmp_path="temp_segment.wav"):
    """Découpe un fichier audio de beat1 jusqu'à beat1 + N mesures, et exécute Basic Pitch dessus."""
    try:
        seconds = measures * (60 / bpm) * 4  # 4 beats/measure
        y, sr = librosa.load(filepath, sr=None, offset=beat1_sec, duration=seconds)
        sf.write(tmp_path, y, sr)

        Brint(f"[TBD] 🎧 Analyse de {tmp_path} (durée {seconds:.2f}s)")
        model_output, midi_data, note_events = predict(
            tmp_path,
            model_or_model_path=ICASSP_2022_MODEL_PATH,
            onset_threshold=0.3,
            frame_threshold=0.3,
            minimum_note_length=30.0,
        )
        return model_output, midi_data, note_events
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def suppress_vlc_warnings():
    
    import warnings
    warnings.filterwarnings("ignore")
#suppress_vlc_warnings()

device = "cuda" if (torch is not None and torch.cuda.is_available()) else "cpu"







Brint("[TBD] ✅ Player lancé depuis :", os.getcwd())


NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def freq_to_note_name(freq):
    if freq <= 0:
        return None
    midi = int(round(69 + 12 * np.log2(freq / 440.0)))
    return NOTE_NAMES[midi % 12]    

def interval_to_degree(note, root):
    circle = NOTE_NAMES * 2
    try:
        i_note = circle.index(note)
        i_root = circle.index(root)
        degree = (i_note - i_root) % 12
        return {
            0: "1", 1: "b2", 2: "2", 3: "b3", 4: "3",
            5: "4", 6: "b5", 7: "5", 8: "b6", 9: "6",
            10: "b7", 11: "7"
        }.get(degree, "?")
    except:
        return "?"

def detect_legato_notes(y, sr, grid_times, window=0.25, hop_length=256):
    f0 = librosa.yin(y, fmin=80, fmax=1000, sr=sr, frame_length=2048, hop_length=hop_length)
    times = librosa.times_like(f0, sr=sr, hop_length=hop_length)
    notes, prev_note, start_time = [], None, None

    for t, freq in zip(times, f0):
        current_note = freq_to_note_name(freq) if freq > 0 else None
        if current_note != prev_note:
            if prev_note and start_time is not None:
                end_time = t
                if (end_time - start_time) >= 0.3:
                    center = (start_time + end_time) / 2
                    notes.append((center, prev_note))
            start_time = t if current_note else None
        prev_note = current_note

    snapped = {}
    for center, note in notes:
        idx = min(range(len(grid_times)), key=lambda i: abs(center - grid_times[i]))
        snapped[idx] = note
    return [snapped.get(i, None) for i in range(len(grid_times))]
def normalize_root(note_name):
    """
    Convertit les noms d'accords avec b (flat) en dièses (#),
    car pretty_midi ne comprend pas les 'b'.
    """
    flat_to_sharp = {
        "Bb": "A#",
        "Eb": "D#",
        "Ab": "G#",
        "Db": "C#",
        "Gb": "F#"
    }
    return flat_to_sharp.get(note_name, note_name)

class LoopData:
        
        
    # --- Nouvelle structure des notes ---
    # Chaque note est définie par son timestamp (en ms) et son contenu

    # Exemple de master_note_list dans LoopData
    # self.master_note_list = [
        # {"timestamp_ms": 2938700, "note": "b"},
        # {"timestamp_ms": 2938900, "note": "7"},
        # {"timestamp_ms": 2940100, "note": "2"},
    # ]

    # --- Fonction de mapping vers subdivision la plus proche ---
    def set_chord_for_measure(self, measure_index, chord):
        beat_pos = measure_index * 4  # assumes 4 beats/measure
        # Trouve et remplace ou crée
        for chord_entry in self.chords:
            if chord_entry["beat_position"] == beat_pos:
                chord_entry["chord"] = chord
                chord_entry["root"] = chord
                return
        self.chords.append({
            "beat_position": beat_pos,
            "chord": chord,
            "root": chord,
            "beat_end": beat_pos + 4
        })

    def set_degree_for_measure(self, measure_index, degree):
        beat_pos = measure_index * 4
        for chord_entry in self.chords:
            if chord_entry["beat_position"] == beat_pos:
                chord_entry["degree"] = degree
                return
        self.chords.append({
            "beat_position": beat_pos,
            "chord": "?",
            "root": "?",
            "degree": degree,
            "beat_end": beat_pos + 4
        })


    
    def get_notes_near_timestamp(self, target_ms, tolerance_ms=50):
        return [n for n in self.master_note_list if abs(n["timestamp_ms"] - target_ms) <= tolerance_ms]

    def add_note_at_timestamp(self, timestamp_ms, note_str, velocity=100):
        # Empêche les doublons exacts
        for note in self.master_note_list:
            if note["timestamp_ms"] == timestamp_ms and note["note"] == note_str:
                return  # déjà présent
        self.master_note_list.append({
            "timestamp_ms": int(note["timestamp_ms"]),
            "note": note_str,
            "velocity": velocity
        })
    def remove_note_at_timestamp(self, timestamp_ms, note_str):
        self.master_note_list = [n for n in self.master_note_list
                                 if not (n["timestamp_ms"] == timestamp_ms and n["note"] == note_str)]

    def map_notes_to_subdivs(self):
        """
        Retourne un dict {subdiv_index: [notes]} où chaque subdivision contient une liste de notes associées.
        Basé sur self.grid_times (en secondes), master_note_list (en millisecondes).
        """
 
        mapping = {i: [] for i in range(len(self.grid_times))}

        for note in self.master_note_list:
            # t_note = note["timestamp_ms"]
            t_note = float(note["timestamp_ms"])

            closest_i = min(
                range(len(self.grid_times)),
                key=lambda i: abs(self.grid_times[i] * 1000 - t_note)
            )
            delta = abs(self.grid_times[closest_i] * 1000 - t_note)
            if delta < 120:  # tolérance à ajuster si besoin
                # mapping[closest_i].append(note["note"])
                # ✅ Bon
                mapping[closest_i].append(note)
                Brint(f"[MAP OK] Note {note['note']} mappée @ subdiv {closest_i} (Δ={delta:.1f}ms)")
            else:
                Brint(f"[MAP SKIP] Note {note['note']} ignorée (Δ={delta:.1f}ms)")

        self.mapped_notes = mapping
        
        total_notes = len(self.master_note_list)
        total_mapped = sum(len(v) for v in mapping.values())
        total_unmapped = total_notes - total_mapped

        if total_mapped == 0:
            Brint(f"[MAP WARN] ❌ 0 notes mappées sur {total_notes} — vérifie unités ou timing de grille")
        elif total_unmapped > 0:
            Brint(f"[MAP INFO] ⚠️ {total_unmapped} note(s) non mappée(s) sur {total_notes}")
        else:
            Brint(f"[MAP OK] ✅ Toutes les {total_notes} notes ont été mappées")
        Brint("[GRID TIMES DEBUG] Subdivisions (ms):")
        for i, t in enumerate(self.grid_times):
            Brint(f"[GRID TIMES DEBUG]  Subdiv {i} → {t*1000:.1f} ms")


        return mapping

    # --- Fonction inverse : enregistrer une note sur une subdivision ---
    def add_note_to_subdiv(self, subdiv_index, note_str):
        """
        Ajoute une note (str) sur une subdivision donnée, convertie en timestamp_ms
        """
        if not hasattr(self, "grid_times") or subdiv_index >= len(self.grid_times):
            Brint(f"[ERROR] Subdiv index {subdiv_index} invalide")
            return
        t_subdiv_ms = int(self.grid_times[subdiv_index] * 1000)  # si grid_times est en sec
        note_obj = {"timestamp_ms": int(t_subdiv_ms), "note": note_str.strip()}
        self.master_note_list.append(note_obj)
        Brint(f"[NOTE] Ajout note '{note_str}' à subdiv {subdiv_index} ({t_subdiv_ms}ms)")




    # --- Fonction utilitaire pour supprimer une note ---
    def remove_note_at_timestamp(self, timestamp_ms, note_str, tolerance_ms=1):
        self.master_note_list = [
            n for n in self.master_note_list
            if not (abs(n["timestamp_ms"] - timestamp_ms) < tolerance_ms and n["note"] == note_str)
        ]


    def get_harmonic_info_by_measure(self, measure_index):
        """Retourne l'accord de la mesure, son degré et sa couleur fonctionnelle"""
        chords = self.get_chords_in_measure(measure_index)
        if not chords:
            return None  # Pas d'accord dans cette mesure

        # On prend le premier accord de la mesure
        chord_data = chords[0]
        beat_pos = chord_data.get("beat_position", measure_index * 4)
        chord = chord_data.get("chord", "")
        key = self.key or "C"
        mode = self.mode or "ionian"

        degree = self.degree_from_chord(chord)
        color = DEGREE_COLOR_MAP.get(degree, "#CCCCCC")  # couleur par défaut

        return {
            "measure": measure_index,
            "beat_pos": beat_pos,
            "key": key,
            "mode": mode,
            "chord": chord,
            "degree": degree,
            "color": color
        }

    
        
    def add_subdivision_and_refresh(self, bp, popup):
        new_beat = bp + 2
        Brint(f"[DEBUG] ➕ Ajout subdivision à beat {new_beat}")
        self.current_loop.update_chord_at_beat(new_beat, "", "")
        self.current_loop.sort_chords()
        popup.destroy()
        self.open_chord_editor_all()


    
    def chord_from_degree(self, degree):
        chord_root = chord_from_degree(degree, self.key or "C", self.mode or "ionian")
        return enhance_chord_from_degree(degree, chord_root)
        
        
    #LOOPDATA INIT

    def __init__(self, name, loop_start, loop_end, key=None, mode=None,
                 chords=None, master_note_list=None, tempo_bpm=None,
                 loop_zoom_ratio=None, confirmed_hit_context=None,
                 hit_timings=None, hit_timestamps=None):
        
        
        
        self.name = name
        self.loop_start = loop_start
        self.loop_end = loop_end
        self.key = key
        self.mode = mode
        self.chords = chords if chords else []
        self.master_note_list = master_note_list if master_note_list else []
        self.tempo_bpm = tempo_bpm  # ✅ Important
        self.loop_zoom_ratio = loop_zoom_ratio if loop_zoom_ratio is not None else .33
        self.confirmed_hit_context = confirmed_hit_context or {
            "timestamps": [],
            "grid_mode": None
        }
        self.hit_timings = hit_timings or []
        self.hit_timestamps = hit_timestamps or []

    @classmethod
    def from_dict(cls, data):
        
        # Normaliser chords
        normalized_chords = []
        for chord in data.get("chords", []):
            if "beat_end" not in chord and "beat_position" in chord:
                chord["beat_end"] = chord["beat_position"] + 4  # valeur par défaut
            normalized_chords.append(chord)


        return cls(
            name=data.get("name", "Unnamed"),
            loop_start=data.get("loop_start"),
            loop_end=data.get("loop_end"),
            key=data.get("key"),
            mode=data.get("mode"),
            chords=normalized_chords,
            master_note_list=data.get("master_note_list", []),
            tempo_bpm=data.get("tempo_bpm") or 60.0,  # ✅ fallback à 60 bpm si None
            loop_zoom_ratio=data.get("loop_zoom_ratio"),
            confirmed_hit_context=data.get("confirmed_hit_context"),
            hit_timings=data.get("hit_timings", []),
            hit_timestamps=data.get("hit_timestamps", [])
        )

    def to_dict(self):
        Brint(f"[TO_DICT DEBUG] tempo_bpm exporté = {self.tempo_bpm}")

        return {
            "name": self.name,
            "loop_start": self.loop_start,
            "loop_end": self.loop_end,
            "key": self.key,
            "mode": self.mode,
            "chords": self.chords,
            "master_note_list": self.master_note_list,
            "tempo_bpm": self.tempo_bpm,  # ✅ Ajouté ici
            "loop_zoom_ratio": self.loop_zoom_ratio,
            "confirmed_hit_context": self.confirmed_hit_context,
            "hit_timings": self.hit_timings,
            "hit_timestamps": self.hit_timestamps
        }
        
        
    def update_chord_at_measure(self, measure_index, chord_name, root_note=None):
        beat_pos = measure_index * 4
        found = next((c for c in self.chords if c.get("beat_position") == beat_pos), None)
        if found:
            found["chord"] = chord_name
            found["root"] = root_note or chord_name
        else:
            self.chords.append({
                "beat_position": beat_pos,
                "chord": chord_name,
                "root": root_note or chord_name
            })

    def degree_from_chord(self, chord):
        if not chord:
            return "?"
        chord_base = chord[0].upper()
        if len(chord) > 1 and chord[1] in ["b", "#"]:
            chord_base += chord[1]

        scale = get_chromatic_scale(self.key or "C")
        try:
            key_index = scale.index((self.key or "C")[0].upper())
            chord_index = scale.index(chord_base)
        except ValueError:
            return "?"

        semitone_distance = (chord_index - key_index) % 12
        mode_degrees = MODES.get(self.mode, MODES["ionian"])
        for i, roman in enumerate(mode_degrees):
            expected_semitone = ROMAN_TO_SEMITONE[roman]
            if expected_semitone == semitone_distance:
                degree = roman
                if chord.lower().endswith("dim"):
                    if "°" not in degree:
                        degree = degree.lower() + "°"
                elif chord.lower().endswith("m"):
                    degree = degree.lower()
                if chord.lower().endswith("7") and "7" not in degree:
                    degree += "7"
                return degree
        return "?"
    def validate(self):
        if self.loop_start is None or self.loop_end is None:
            return False, "Loop start ou end manquant"
        if self.loop_start >= self.loop_end:
            return False, "Loop start >= loop end"
        return True, None

    def get_chords_in_measure(self, measure_index):
        """Retourne toutes les subdivisions d'accords dans une mesure."""
        beat_start = measure_index * 4
        beat_end = beat_start + 4
        return [c for c in self.chords if beat_start <= c.get("beat_position", -1) < beat_end]

    def update_chord_at_beat(self, beat_position, chord_name, root_note=None):
        """Ajoute ou remplace un accord à un beat exact."""
        found = next((c for c in self.chords if c.get("beat_position") == beat_position), None)
        if found:
            found["chord"] = chord_name
            found["root"] = root_note or chord_name
        else:
            self.chords.append({
                "beat_position": beat_position,
                "chord": chord_name,
                "root": root_note or chord_name
            })

    def remove_chord_at_beat(self, beat_position):
        """Supprime un accord à un beat exact."""
        self.chords = [c for c in self.chords if c.get("beat_position") != beat_position]

    def get_chord_at_beat(self, beat_position):
        """Retourne l'accord actif à un beat (même fractionnaire), basé sur beat_position ∈ [start, end)."""
        if not self.chords:
            Brint(f"[CHORD LOOKUP] ❌ Aucun accord dans self.chords pour beat {beat_position}")
            return None

        for chord in self.chords:
            start = chord.get("beat_position")
            end = chord.get("beat_end")

            if start is None:
                continue  # skip if malformed

            # fallback si beat_end absent
            if end is None:
                Brint(f"[CHORD LOOKUP] ⚠️ Accord sans beat_end : {chord}")
                end = start + 4

            if start <= beat_position < end:
                Brint(f"[CHORD LOOKUP] ✅ Beat {beat_position:.2f} ∈ [{start}, {end}) ➜ {chord}")
                return chord

        Brint(f"[CHORD LOOKUP] 🔍 Aucun accord trouvé pour beat {beat_position:.2f}")
        return None

    def sort_chords(self):
        """Tri les accords par beat_position croissante."""
        self.chords = sorted(self.chords, key=lambda c: c.get("beat_position", 0))


class ToolTip:
    def __init__(self, widget, text='info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class VideoPlayer:
    
    def timestamp_to_subdiv_index(self, timestamp_ms, grid_times):
        if not grid_times:
            return None
        return min(range(len(grid_times)), key=lambda i: abs(grid_times[i] - timestamp_ms))

    def subdiv_index_to_timestamp(self, subdiv_index, grid_times):
        if 0 <= subdiv_index < len(grid_times):
            return grid_times[subdiv_index]
        return None
    
    
    def try_itemconfig(self, canvas_widget, item_id, **kwargs):
        # Helper to safely call itemconfig, catching TclError if item is gone.
        try:
            canvas_widget.itemconfig(item_id, **kwargs)
        except tk.TclError:
            # Optional: Log this occurrence if it's unexpected.
            # Brint(f"[HIT_FX_ANIM_WARN] Item {item_id} no longer exists for itemconfig: {kwargs}")
            pass # Item was already deleted, which is fine.

    def _remove_impact_vfx(self, line_id):
        try:
            if self.grid_canvas: # Ensure canvas itself exists
                self.grid_canvas.delete(line_id)
            if line_id in self.impact_strikes:
                self.impact_strikes.remove(line_id)
            # Brint(f"[HIT FX] ✅ Impact visuel retiré (line_id={line_id})") # Keep or silence this
        except tk.TclError:
            # Brint(f"[HIT FX_REMOVE_WARN] Item {line_id} no longer exists for delete.")
            pass # Item was already deleted.
    
    def match_hits_to_subdivs(self):
        from collections import defaultdict

        dynamic_hits = defaultdict(int)

        if not hasattr(self, "user_hit_timestamps") or not self.user_hit_timestamps:
            return dynamic_hits

        if not self.precomputed_grid_infos:
            self.compute_rhythm_grid_infos()

        if not self.precomputed_grid_infos:
            return dynamic_hits

        sorted_items = sorted(
            self.precomputed_grid_infos.items(),
            key=lambda item: item[1]['t_subdiv_sec']
        )
        sorted_times = [info['t_subdiv_sec'] for _, info in sorted_items]
        sorted_indices = [idx for idx, _ in sorted_items]

        intervals = [t2 - t1 for t1, t2 in zip(sorted_times[:-1], sorted_times[1:])]
        avg_interval_sec = sum(intervals) / len(intervals) if intervals else 0.5
        # Widen the detection window so every hit can match a subdivision
        tolerance = avg_interval_sec / 2.0
        Brint(f"[HIT WINDOW] ℹ️ Tolerance set to {tolerance:.3f}s (1/2 of {avg_interval_sec:.3f}s)")

        loop_duration_s = None
        if (
            hasattr(self, "loop_end")
            and hasattr(self, "loop_start")
            and self.loop_end is not None
            and self.loop_start is not None
        ):
            loop_duration_s = (self.loop_end - self.loop_start) / 1000.0

        for t_hit, _loop_pass in self.user_hit_timestamps:
            t_norm = t_hit

            closest_pos, closest_t = min(
                enumerate(sorted_times),
                key=lambda item: abs(item[1] - t_norm)
            )
            delta = abs(closest_t - t_norm)
            if delta <= tolerance:
                closest_i = sorted_indices[closest_pos]
                dynamic_hits[closest_i] += 1
                Brint(
                    f"[HIT MAP] 🟠 t_hit={t_hit:.3f}s → Subdiv {closest_i} (Δ={delta:.3f}s)"
                )
            else:
                Brint(
                    f"[HIT MAP] ⛔ t_hit={t_hit:.3f}s ignoré (Δ={delta:.3f}s > tolérance)"
                )

        return dynamic_hits

    def maybe_adjust_zoom_if_out_of_frame(self):
        """
        Vérifie si loop_start ou loop_end sortent de la zone visible actuelle (5%–95%).
        Si oui, déclenche auto_zoom_on_loop_markers().
        Sinon, ne touche pas au zoom.
        """
        if not self.loop_start or not self.loop_end:
            return

        zoom = self.get_zoom_context()
        z_start = zoom["zoom_start"]
        z_end = zoom["zoom_end"]
        z_range = zoom["zoom_range"]

        loop_duration = self.loop_end - self.loop_start
        zoom_range = self.get_zoom_context()["zoom_range"]

        if z_range < loop_duration:
            Brint("[ZOOM CHECK] ➖ Zoom inférieur à la boucle, aucune réinitialisation")
            return

        if loop_duration > 0 and zoom_range > 0:
            ratio = zoom_range / loop_duration
            Brint(f"[ZOOM CHECK] 📏 Ratio zoom/loop = {ratio:.2f}")

            if ratio > 10.0:  # par exemple, si le zoom affiche plus de 10x la boucle
                Brint("[ZOOM CHECK] ⚠️ Zoom trop large pour la boucle → auto zoom")
                self.auto_zoom_on_loop_markers()


        margin_start = z_start + int(0.05 * z_range)
        margin_end = z_start + int(0.95 * z_range)

        Brint(f"[ZOOM CHECK] 🎯 Fenêtre visible = {z_start} → {z_end} (range={z_range})")
        Brint(f"[ZOOM CHECK] 🔍 Marges 5–95% = {margin_start} → {margin_end}")
        Brint(f"[ZOOM CHECK] 🅰️ A = {self.loop_start} | 🅱️ B = {self.loop_end}")

        # Save previous zoom to detect changes
        prev_zoom = zoom
        prev_A_x = self.time_sec_to_canvas_x(self.loop_start / 1000.0)
        prev_B_x = self.time_sec_to_canvas_x(self.loop_end / 1000.0)

        # Decision
        if self.loop_start < margin_start:
            Brint("[ZOOM CHECK] 🅰️ A trop à gauche → zoom recalc")
            self.auto_zoom_on_loop_markers()
        elif self.loop_end > margin_end:
            Brint("[ZOOM CHECK] 🅱️ B trop à droite → zoom recalc")
            self.auto_zoom_on_loop_markers()
        else:
            Brint("[ZOOM CHECK] ✅ A et B visibles dans la fenêtre actuelle → zoom conservé")
            return

        # Post check
        new_zoom = self.get_zoom_context()
        new_A_x = self.time_sec_to_canvas_x(self.loop_start / 1000.0)
        new_B_x = self.time_sec_to_canvas_x(self.loop_end / 1000.0)

        Brint(f"[ZOOM MOVE] 🔁 Zoom modifié !")
        Brint(f"[TBD]   🎯 A: x avant = {prev_A_x}px → après = {new_A_x}px")
        Brint(f"[TBD]   🎯 B: x avant = {prev_B_x}px → après = {new_B_x}px")
        Brint(f"  🔍 zoom_start: {prev_zoom['zoom_start']} → {new_zoom['zoom_start']}")
        Brint(f"  🔍 zoom_range: {prev_zoom['zoom_range']} → {new_zoom['zoom_range']}")



    def auto_zoom_on_loop_markers(self, force=False):
        """
        Ajuste le zoom automatiquement selon l'état de loop_start et loop_end :
        - Si A seul est défini, zoom sur A + 1min avec A à 20%.
        - Si A et B sont définis, zoom pour que A soit à 20% et B à 80%.
        """
        video_duration = self.player.get_length()

        if not self.loop_start:
            Brint("[AUTOZOOM] ❌ loop_start manquant → pas de zoom possible")
            return

        Brint(f"[AUTOZOOM] 🎬 Durée vidéo = {video_duration} ms")

        if not self.loop_end or self.loop_end <= self.loop_start:
            Brint("[AUTOZOOM] 🅰️ seul défini → zoom A à 20% sur 1 minute")

            zoom_range_ms = 60000
            zoom_start_ms = self.loop_start - int(0.2 * zoom_range_ms)
            zoom_end_ms = zoom_start_ms + zoom_range_ms

            Brint(f"[AUTOZOOM] 📐 Calcul initial : zoom_start={zoom_start_ms}, zoom_end={zoom_end_ms}")

            if zoom_start_ms < 0:
                zoom_start_ms = 0
                zoom_end_ms = zoom_range_ms
                Brint("[AUTOZOOM] 🔧 Clamp gauche : zoom_start ajusté à 0")

            if zoom_end_ms > video_duration:
                zoom_end_ms = video_duration
                zoom_start_ms = max(0, video_duration - zoom_range_ms)
                Brint("[AUTOZOOM] 🔧 Clamp droite : zoom_end ajusté à durée vidéo")

            self.zoom_context = {
                "zoom_start": zoom_start_ms,
                "zoom_end": zoom_end_ms,
                "zoom_range": zoom_end_ms - zoom_start_ms
            }

            self.loop_end = self.loop_start + zoom_range_ms
            self.loop_zoom_ratio = zoom_range_ms / self.zoom_context["zoom_range"]

            self.console.config(text="🅰️ Zoom auto : A à 20%, durée 1min")
            Brint(f"[AUTOZOOM] ✅ Zoom défini pour A seul : start={zoom_start_ms}, end={zoom_end_ms}, ratio={self.loop_zoom_ratio:.3f}")

        else:
            Brint("[AUTOZOOM] 🅰️ + 🅱️ définis → zoom A à 20%, B à 80%")

            loop_len = self.loop_end - self.loop_start
            if loop_len <= 0:
                Brint("[AUTOZOOM] ❌ Loop invalide (B < A)")
                return

            zoom_range = int(max(loop_len / 0.6, MIN_ZOOM_RANGE_MS))
            # 💡 Limite de zoom max : on ne veut pas zoomer sur toute la vidéo
            max_zoom_range = min(video_duration, 300000)  # 5 minutes max

            if zoom_range > max_zoom_range:
                Brint(f"[AUTOZOOM] ⚠️ zoom_range trop grand ({zoom_range}) → clamp à {max_zoom_range}")
                zoom_range = max_zoom_range

            
            zoom_start = self.loop_start - int(0.2 * zoom_range)
            zoom_end = zoom_start + zoom_range

            Brint(f"[AUTOZOOM] 📐 Calcul initial : zoom_start={zoom_start}, zoom_end={zoom_end}, zoom_range={zoom_range}")

            if zoom_start < 0:
                zoom_start = 0
                zoom_end = zoom_range
                Brint("[AUTOZOOM] 🔧 Clamp gauche : zoom_start ajusté à 0")

            if zoom_end > video_duration:
                zoom_end = video_duration
                zoom_start = max(0, video_duration - zoom_range)
                Brint("[AUTOZOOM] 🔧 Clamp droite : zoom_end ajusté à durée vidéo")

            self.zoom_context = {
                "zoom_start": zoom_start,
                "zoom_end": zoom_end,
                "zoom_range": zoom_end - zoom_start
            }

            self.loop_zoom_ratio = loop_len / self.zoom_context["zoom_range"]
            self.console.config(text="🔍 Zoom auto : A à 20%, B à 80%")

            Brint(f"[AUTOZOOM] ✅ Zoom défini A+B : start={zoom_start}, end={zoom_end}, ratio={self.loop_zoom_ratio:.3f}")

        if hasattr(self, "zoom_ratio_var"):
            self.zoom_ratio_var.set(self.loop_zoom_ratio)

        self.update_loop()
     

 
    def reset_rhythm_overlay(self):
        if not hasattr(self, "grid_canvas"):
            return
        self.grid_canvas.delete("rhythm_grid")
        self.grid_canvas.delete("syllabic_label")
        self.grid_canvas.delete("syllabic_hit")
        self.grid_canvas.delete("heatmap_filtered")
        Brint("[RHYTHM OVERLAY] 🧼 Canvas nettoyé")
    
    def is_loop_effectively_defined(self):
        """
        Retourne True seulement si A et B sont définis,
        A > 0 et B < duration → boucle réellement définie.
        """
        duration = self.player.get_length()

        if self.loop_start is None or self.loop_end is None:
            return False

        return self.loop_start > 0 and self.loop_end < duration


    def is_loop_fully_cleared(self):
        return self.loop_start == 0 and self.loop_end == self.player.get_length()

    
    
    def cycle_note_display_mode(self):
        """Fait cycler l'affichage des notes : key-relative → chord-relative → absolute"""
        modes = ["key", "chord", "absolute"]
        current = getattr(self, "harmony_note_display_mode", "key")
        next_mode = modes[(modes.index(current) + 1) % len(modes)]
        self.harmony_note_display_mode = next_mode

        Brint(f"\n[DISPLAY MODE] 🔁 Passage du mode '{current}' → '{next_mode}'")

        if next_mode == "key":
            Brint("[TBD]   ➤ Les intervalles seront calculés par rapport à la tonalité globale (key).")
        elif next_mode == "chord":
            Brint("[TBD]   ➤ Les intervalles seront calculés par rapport à l’accord actif de la mesure.")
        elif next_mode == "absolute":
            Brint("[TBD]   ➤ Affichage absolu : les notes sont colorées sans relation harmonique.")
        else:
            Brint("[TBD]   ⚠️ Mode inconnu, fallback 'key'")

        # Rafraîchit l’affichage
        self.draw_rhythm_grid_canvas()
        self.draw_harmony_grid_overlay()
    
    def extend_chords_to_fit_loop(self):
        if not hasattr(self, "current_loop") or not self.current_loop:
            Brint("[CHORD EXTEND] ❌ Pas de boucle active")
            return

        bpm = self.get_effective_bpm()
        loop = self.current_loop
        duration_s = (loop.loop_end - loop.loop_start) / 1000.0
        total_beats = int(duration_s * (bpm / 60.0))

        if not hasattr(loop, "chords") or not loop.chords:
            loop.chords = []

        defined_ranges = []
        for chord in loop.chords:
            start = chord.get("beat_position", 0)
            end = chord.get("beat_end", start + 4)
            defined_ranges.append((start, end))

        # Flatten les ranges définis
        defined_beats = set()
        for start, end in defined_ranges:
            defined_beats.update(range(int(start), int(end)))

        default_root = loop.key if getattr(loop, "key", None) else "C"
        default_chord = {
            "chord": default_root,
            "root": default_root,
            "degree": "I"  # optionnel
        }

        # Étendre en blocs de 4 temps
        next_beat = 0
        while next_beat < total_beats:
            if next_beat not in defined_beats:
                loop.chords.append({
                    **default_chord,
                    "beat_position": next_beat,
                    "beat_end": next_beat + 4,
                    "autopad": True  # 🟩 on marque l'accord comme ajouté automatiquement
                })
                Brint(f"[CHORD EXTEND] Ajout accord par défaut {default_root} de beat {next_beat} à {next_beat + 4} [autopad]")
            next_beat += 4

    
    def compute_mapped_notes(self):
        if not hasattr(self, "grid_subdivs") or not self.grid_subdivs:
            Brint("[MAP NOTES] ❌ Pas de subdivisions pour mapper les notes.")
            return

        if not hasattr(self.current_loop, "master_note_list"):
            Brint("[MAP NOTES] ❌ Pas de note list dans current_loop.")
            return

        self.current_loop.mapped_notes = {i: [] for i in range(len(self.grid_subdivs))}

        for note in self.current_loop.master_note_list:
            t_note_sec = note["timestamp_ms"] / 1000.0
            closest_i = min(
                range(len(self.grid_subdivs)),
                key=lambda i: abs(self.grid_subdivs[i][1] - t_note_sec)
            )
            self.current_loop.mapped_notes[closest_i].append(note)

    
    def remap_chords_by_time(self):
        """
        Recalcule la liste d'accords alignée sur la nouvelle grille RHYTHMique,
        en se basant sur les timestamps des anciens accords (en beats),
        et sur le temps des beats dans la nouvelle subdivision.
        """
        if not hasattr(self.current_loop, "chords") or not self.current_loop.chords:
            Brint("[remap_chords_by_time] ⚠️ Aucun accord à remapper.")
            return []

        bpm = self.get_effective_bpm()
        loop_start_ms = self.current_loop.loop_start
        grid_times_sec = [t for _, t in self.grid_subdivs]
        grid_times_ms = [int(t * 1000) for t in grid_times_sec]

        # Reconstitue les temps des beats à partir des grid_subdivs

        subdivisions_per_beat = self.get_subdivisions_per_beat()


        beats = []
        for i in range(0, len(grid_times_sec), subdivisions_per_beat):
            if i < len(grid_times_sec):
                t = grid_times_sec[i]
                beats.append((i, t))  # (index_subdiv, time_sec)

        # Remap des accords par temps
        new_chords = []
        old_chords = self.current_loop.chords

        for chord in old_chords:
            beat_pos = chord.get("beat_position", 0)
            beat_start_ms = loop_start_ms + (beat_pos * 60_000 / bpm)

            # Cherche le beat actuel dont le timestamp est le plus proche
            closest_beat = min(beats, key=lambda b: abs((b[1]*1000 + loop_start_ms) - beat_start_ms))
            new_beat_index = beats.index(closest_beat)

            new_chords.append({
                "chord": chord.get("chord", "?"),
                "degree": chord.get("degree", "?"),
                "beat_position": new_beat_index,
                # optionnel : recalcul beat_end ? ou le conserver tel quel
            })

        Brint(f"[remap_chords_by_time] ✅ {len(new_chords)} accords remappés sur {len(beats)} beats")
        return new_chords

    
    
    def get_zoom_context(self):
        """
        Si zoom_context est défini manuellement, on l’utilise.
        Sinon, fallback dynamique basé sur loop + zoom_ratio.
        """
        if getattr(self, "reset_zoom_next_frame", False):
            self.reset_zoom_next_frame = False
            if hasattr(self, "zoom_context") and self.zoom_context:
                return dict(self.zoom_context)
            duration = self.player.get_length() if hasattr(self, "player") else 0
            return {"zoom_start": 0, "zoom_end": duration, "zoom_range": duration}
        if hasattr(self, "zoom_context") and self.zoom_context:
            base_zoom = dict(self.zoom_context)
        else:
            base_zoom = None

        loop_start = self.loop_start or 0
        loop_end = self.loop_end or self.duration or 10000  # fallback sécurité
        loop_width = loop_end - loop_start
        zoom_ratio = self.loop_zoom_ratio or 1.0
        zoom_width = int(loop_width / zoom_ratio)

        zoom_center = (loop_start + loop_end) // 2
        zoom_start = zoom_center - zoom_width // 2
        zoom_end = zoom_start + zoom_width

        # 🔒 CLAMP de sécurité
        video_duration = self.player.get_length() if hasattr(self, "player") else 100000
        if zoom_start < 0:
            zoom_start = 0
            zoom_end = zoom_width
        if zoom_end > video_duration:
            zoom_end = video_duration
            zoom_start = max(0, zoom_end - zoom_width)

        zoom_dict = {
            "zoom_start": zoom_start,
            "zoom_end": zoom_end,
            "zoom_width": zoom_width,
            "zoom_range": zoom_width  # alias
        }

        if base_zoom is not None:
            zoom_dict.update(base_zoom)

        progress_raw = None
        if (
            self.loop_start is not None
            and self.loop_end is not None
            and getattr(self, "playhead_time", None) is not None
        ):
            playhead_ms = self.playhead_time * 1000.0
            loop_range = self.loop_end - self.loop_start
            if loop_range > 0:
                progress_raw = (playhead_ms - self.loop_start) / loop_range

        editing_loop = False
        if hasattr(self, "edit_mode") and hasattr(self.edit_mode, "get"):
            try:
                editing_loop = self.edit_mode.get() in ("loop_start", "loop_end")
            except Exception:
                editing_loop = False

        dynamic_condition = (
            base_zoom is not None
            and progress_raw is not None
            and base_zoom.get("zoom_range", 0) < (self.loop_end - self.loop_start) / 0.9
            and not editing_loop
        )

        if dynamic_condition:
            if progress_raw < 0 or progress_raw > 1:
                zoom_dict["zoom_start"] = (self.loop_start + self.loop_end - base_zoom["zoom_range"]) / 2
                zoom_dict["zoom_end"] = zoom_dict["zoom_start"] + base_zoom["zoom_range"]
            else:
                offset = progress_raw * (loop_range - 0.9 * base_zoom["zoom_range"])
                zoom_dict["zoom_start"] = self.loop_start + offset
                zoom_dict["zoom_end"] = zoom_dict["zoom_start"] + base_zoom["zoom_range"]
        elif progress_raw is not None and base_zoom is not None and (progress_raw < 0 or progress_raw > 1):
            zoom_dict["zoom_start"] = (self.loop_start + self.loop_end - base_zoom["zoom_range"]) / 2
            zoom_dict["zoom_end"] = zoom_dict["zoom_start"] + base_zoom["zoom_range"]

        if base_zoom is not None:
            zoom_width = base_zoom["zoom_range"]
            if zoom_dict["zoom_start"] < 0:
                zoom_dict["zoom_start"] = 0
                zoom_dict["zoom_end"] = zoom_width
            if zoom_dict["zoom_end"] > video_duration:
                zoom_dict["zoom_end"] = video_duration
                zoom_dict["zoom_start"] = max(0, video_duration - zoom_width)

        return zoom_dict


    def rebuild_loop_context(self):
        Brint("[DEBUG rebuild_loop_context] 🔁 Reconstruction contexte boucle")
        self.build_rhythm_grid()
        self.draw_rhythm_grid_canvas()
        self.compute_rhythm_grid_infos()
        self.grid_subdivs = [(i, t) for i, t in enumerate(self.grid_times)]
        self.current_loop.grid_times = self.grid_times
        self.current_loop.grid_subdivs = self.grid_subdivs
        self.debug_grid_subdivs("rebuild_loop_context")
        # self.current_loop.chords = self.remap_chords_by_time()


        if hasattr(self.current_loop, "map_notes_to_subdivs"):
            Brint("[REMAP rebuild_loop_context] 🎵 Mapping des notes aux subdivisions")
            self.current_loop.mapped_notes = self.current_loop.map_notes_to_subdivs()
            Brint(f"[REMAP rebuild_loop_context] ✅ {sum(len(v) for v in self.current_loop.mapped_notes.values())} notes mappées")
        Brint(f"[DEBUG rebuild_loop_context] grid_times = {self.grid_times[:3]}... ({len(self.grid_times)} total)")
        Brint(f"[DEBUG rebuild_loop_context] grid_subdivs = {len(self.grid_subdivs)} subdivisions générées")


    def set_zoom_range_from_loop(self, loop):
        """
        ⚠️ Obsolète : GlobXa / GlobXb sont désormais supprimés.
        Le zoom se base directement sur loop_start et loop_zoom_ratio dans les fonctions de conversion.
        """
        Brint("[ZOOM INIT set_zoom_range_from_loop] 🚫 Fonction ignorée (GlobXa/GlobXb supprimés)")
        return

        
    def debug_grid_subdivs(self, source=""):
        import inspect
        caller = inspect.stack()[1].function
        Brint(f"[TRACE GRID] 🧩 Assigné par '{caller}' {f'→ {source}' if source else ''}")

        if (not hasattr(self, "loop_start") or self.loop_start is None or
            not hasattr(self, "loop_end") or self.loop_end is None or
            self.tempo_bpm is None):
            Brint("[TRACE GRID ERROR] ❌ loop_start, loop_end ou tempo_bpm manquant — grille non générée")
            self.grid_subdivs = []
            return

        loop_start_sec = self.loop_start / 1000.0
        loop_end_sec = self.loop_end / 1000.0
        duration_sec = loop_end_sec - loop_start_sec
        if duration_sec <= 0:
            Brint("[TRACE GRID ERROR] ❌ Durée de loop invalide")
            self.grid_subdivs = []
            return


        subdivisions_per_beat = self.get_subdivisions_per_beat()

        interval_sec = 60.0 / self.tempo_bpm / subdivisions_per_beat
        n_subdivs = int(duration_sec / interval_sec)

        self.grid_subdivs = [(i, loop_start_sec + i * interval_sec) for i in range(n_subdivs)]

        Brint(f"[TRACE GRID] ✅ Généré {len(self.grid_subdivs)} subdivisions via debug fallback")
        Brint(f"[TRACE GRID] Extrait: {self.grid_subdivs[:3]}")
            

    def add_note_event(self, timestamp_ms, note, velocity=100):
        self.master_note_list.append({
            "timestamp_ms": float(timestamp_ms),
            "note": note,
            "velocity": velocity
        })


    
    def remove_notes_in_range(self, start_ms, end_ms):
        self.master_note_list = [
            note for note in self.master_note_list
            if not (start_ms <= note["timestamp_ms"] < end_ms)
        ]

    
    
    def get_notes_near_timestamp(self, target_ms, tolerance_ms=100):
        return [
            note for note in self.master_note_list
            if abs(note["timestamp_ms"] - target_ms) <= tolerance_ms
        ]

    
    def format_note_label(self, note, display_mode="absolute", context_chord=None, context_key=None):
        if display_mode == "absolute":
            return note
        elif display_mode == "relative_key" and context_key:
            return get_interval_from_key(note, context_key)  # à coder selon ta logique
        elif display_mode == "relative_chord" and context_chord:
            return get_interval_from_chord(note, context_chord)  # idem
        else:
            return note


    def cycle_chord_harmony_mode(self) :
        self.harmony_chord_display_mode = ("chord" if self.harmony_chord_display_mode == "degree" else "degree")
        Brint(f"[KEYBOARD] 🔁 Chord label mode → {self.harmony_chord_display_mode}")
        self.draw_rhythm_grid_canvas()
        
    def cycle_note_harmony_mode(self) : 
        modes = ["absolute", "relative_key", "relative_chord"]
        current = self.harmony_note_display_mode
        idx = (modes.index(current) + 1) % len(modes)
        self.harmony_note_display_mode = modes[idx]
        Brint(f"[KEYBOARD] 🔁 Note display mode → {self.harmony_note_display_mode}")
        self.draw_rhythm_grid_canvas()
        
        
    def toggle_harmony_display_mode(self, event=None):
        self.harmony_chord_display_mode = "degree" if self.harmony_chord_display_mode == "chord" else "chord"
        pass#Brint(f"[HARMONY] 🔁 Mode accord = {self.harmony_chord_display_mode}")
        self.draw_rhythm_grid_canvas()

    def toggle_note_display_mode(self, event=None):
        next_mode = {"absolute": "rel_key", "rel_key": "rel_chord", "rel_chord": "absolute"}
        self.harmony_note_display_mode = next_mode[self.harmony_note_display_mode]
        Brint(f"[NOTES] 🔁 Mode note = {self.harmony_note_display_mode}")
        self.draw_rhythm_grid_canvas()


    
    
    def update_tempo_ui_from_loop(self):
        if hasattr(self.current_loop, "tempo_bpm") and self.current_loop.tempo_bpm:
            self.tempo_bpm = self.current_loop.tempo_bpm
            self.tempo_var.set(round(self.tempo_bpm, 2))
            ms_per_beat = round(60000 / self.tempo_bpm, 1)
            self.tempo_label.config(text=f"{self.tempo_bpm:.2f} BPM • {ms_per_beat} ms/beat")
            Brint(f"[UI SYNC] tempo_bpm UI mis à jour depuis current_loop : {self.tempo_bpm}")

    def get_effective_bpm(self):
        return getattr(self.current_loop, "tempo_bpm", None) or 60.0

    
    def beat_to_canvas_x(self, beat):
        if beat is None:
            Brint("[ERROR] ❌ beat_to_canvas_x() appelé avec beat=None")
            return 0  # ou None ou -1, selon ton usage

        bpm = self.get_effective_bpm()
        Brint(f"[TRACE] bpm utilisé = {bpm}")
        t_sec = (self.current_loop.loop_start / 1000.0) + (beat * 60.0 / bpm)
        return self.time_sec_to_canvas_x(t_sec)


    def time_sec_to_canvas_x(self, t_sec, use_margin=True, *, zoom=None, canvas_width=None):
        import traceback
        # Brint(f"[DEBUG time_sec_to_canvas_x] → Appel avec t_sec={t_sec}")
        # traceback.print_stack(limit=5)

        t_ms = t_sec * 1000

        loop_start = self.loop_start or 0
        loop_end = self.loop_end or 0

        if loop_end <= loop_start:
            loop_start = 0
            loop_end = self.player.get_length()
            Brint(f"[INFO Time2X] Pas de loop active, fallback à toute la durée ({loop_end} ms) avec zoom_ratio={self.loop_zoom_ratio}")

        loop_range = loop_end - loop_start
        if zoom is None:
            zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_range = zoom["zoom_range"]

        if canvas_width is None:
            canvas_width = getattr(self, "cached_canvas_width", self.grid_canvas.winfo_width())
        if canvas_width <= 1:
            Brint(f"[WARNING] canvas_width trop petit ({canvas_width}), fallback 100")
            canvas_width = 100

        if zoom_range <= 0:
            Brint(f"[WARNING] zoom_range invalide ({zoom_range}), fallback 1000")
            zoom_range = 1000

        ratio = (t_ms - zoom_start) / zoom_range
        if zoom_range < loop_range and use_margin:
            x = 0.05 * canvas_width + ratio * 0.90 * canvas_width
        else:
            x = ratio * canvas_width

        # The raw canvas position may lie outside the visible range when zoomed.
        # Return this unclamped value so callers can decide how to handle it.
        Brint("[TBD]", t_sec, zoom_range, loop_range, ratio, x)
        x = round(x)

        Brint(f"[DEBUG time_sec_to_canvas_x] t_sec={t_sec:.3f}s | t_ms={t_ms:.1f} | zoom_start={zoom_start} | zoom_range={zoom_range} | canvas_width={canvas_width} → x={x}")
        return x

    def zoom_pref_path_for_current_media(self):
        if not hasattr(self, "current_path") or not self.current_path:
            Brint("[ZOOM PREFS] ⚠️ current_path est vide, fallback sur zoom_default.json")
            return "zoom_default.json"

        base = os.path.basename(self.current_path)
        name, _ = os.path.splitext(base)
        zoom_dir = "zoom_prefs"
        path = os.path.join(zoom_dir, f"{name}_zoom.json")
        Brint(f"[ZOOM PREFS] 📁 Fichier zoom associé = {path}")
        return path

    def save_screen_zoom_prefs(self):
        os.makedirs("zoom_prefs", exist_ok=True)
        path = self.zoom_pref_path_for_current_media()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "global_zoom_level": self.global_zoom_level,
                    "global_crop_x": self.global_crop_x,
                }, f, indent=2)
            Brint(f"[ZOOM PREFS] 💾 Zoom sauvegardé dans : {path} | zoom_level = {self.global_zoom_level:.2f}, crop_x = {self.global_crop_x}")
        except Exception as e:
            Brint(f"[ZOOM PREFS] ❌ Erreur lors de la sauvegarde dans {path} : {e}")


    def load_screen_zoom_prefs(self):
        Brint("[ZOOM PREFS]")
        path = self.zoom_pref_path_for_current_media()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.global_zoom_level = data.get("global_zoom_level", 1.0)
                    self.global_crop_x = data.get("global_crop_x", 0.0)
                Brint(f"[ZOOM PREFS] ✅ Zoom chargé depuis : {path} | zoom_level = {self.global_zoom_level:.2f}, crop_x = {self.global_crop_x}")
            except Exception as e:
                Brint(f"[ZOOM PREFS] ❌ Erreur lecture fichier zoom : {e}")
                self.global_zoom_level = 1.0
                self.global_crop_x = 0.0
        else:
            Brint(f"[ZOOM PREFS] 📭 Aucun fichier trouvé pour {path}, zoom réinitialisé")
            self.global_zoom_level = 1.0
            self.global_crop_x = 0.0
      
   
   
   
   
   
   
   
   
   
   
        
        
        
    def media_path_from_abloops(self, abloops_path):
        base = os.path.basename(abloops_path)
        if not base.startswith(".") or not base.endswith(".abloops.json"):
            return None  # format non valide

        media_filename = base[1:-13]  # strip "." + ".abloops.json"
        media_dir = os.path.dirname(abloops_path)

        for ext in [".mp4", ".m4a", ".mov", ".wav"]:
            candidate = os.path.join(media_dir, media_filename + ext)
            if os.path.exists(candidate):
                return candidate

        return None  # aucun fichier trouvé

    
    def set_loop_by_name(self, name):
        
        Brint(f"[DEBUG] Entrée dans set_loop_by_name('{name}')")
        self.update_tempo_ui_from_loop()

        if not self.saved_loops:
            Brint("[LOOP] ❌ Aucune boucle chargée")
            return

        # Sécurité : strip et lowercase pour comparaison souple
        target = name.strip().lower()

        for i, loop_dict in enumerate(self.saved_loops):
            Brint(f"[DEBUG] Comparaison : '{loop_dict.get('name')}' vs '{name}'")

            loop_name = loop_dict.get("name", "").strip().lower()
            if loop_name == target:
                Brint(f"[LOOP] ✅ Boucle trouvée : {loop_dict.get('name')} (index {i})")
                self.load_saved_loop(i)
                return

        Brint(f"[LOOP] ❌ Boucle « {name} » introuvable dans saved_loops")



    def try_auto_load_recent_file(self, index=0, path=None):
        try:
            with open(RECENT_FILES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "recent_paths": [],
                "last_loops": {},
                "auto_load_last_file": True,
                "auto_load_last_loop": True,
            }
            try:
                with open(RECENT_FILES_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                Brint("[AUTOLOAD] 🌱 Création de recent_files.json")
            except Exception as e:
                Brint(f"[AUTOLOAD] ❌ Impossible de créer recent_files.json : {e}")
        except Exception as e:
            import traceback
            Brint(f"[AUTOLOAD] ❌ Erreur autoload : {e}")
            traceback.print_exc()
            return


        if path:
            if not os.path.exists(path):
                Brint(f"[AUTOLOAD] ❌ Média introuvable : {path}")
                return

            self.open_given_file(path)
            self.current_path = path
            Brint(f"[AUTOLOAD] ✅ Média ouvert : {path}")

            if data.get("auto_load_last_loop"):
                loop_name = data.get("last_loops", {}).get(path)
                if loop_name:
                    self.root.after(500, lambda: self.set_loop_by_name(loop_name))
                    Brint(f"[AUTOLOAD] ⏳ Boucle à restaurer : {loop_name}")
                else:
                    Brint("[AUTOLOAD] ℹ️ Aucune boucle à restaurer pour ce média")
            return

        if not data.get("auto_load_last_file"):
            Brint("[AUTOLOAD] ⏩ Autoload désactivé")
            return

        paths = data.get("recent_paths", [])
        if not paths:
            Brint("[AUTOLOAD] ❌ Aucun chemin récent")
            return

        if index >= len(paths) or index < 0:
            Brint(f"[AUTOLOAD] ❌ Index {index} hors limite")
            return

        media_path = paths[index]
        if not os.path.exists(media_path):
            Brint(f"[AUTOLOAD] ❌ Média introuvable : {media_path}")
            return

        # 🎞️ Étape 1 : ouvrir le fichier média
        self.open_given_file(media_path)
        self.current_path = media_path
        Brint(f"[AUTOLOAD] ✅ Média ouvert : {media_path}")

        # 📄 Étape 2 : charger les boucles depuis le .abloops.json dérivé
        self.load_saved_loops()

        # 🔁 Étape 3 : charger la dernière loop associée à ce fichier
        if data.get("auto_load_last_loop"):
            loop_name = data.get("last_loops", {}).get(media_path)
            if loop_name:
                self.root.after(500, lambda: self.set_loop_by_name(loop_name))
                Brint(f"[AUTOLOAD] ⏳ Boucle à restaurer : {loop_name}")
            else:
                Brint("[AUTOLOAD] ℹ️ Aucune boucle à restaurer pour ce média")

    def quick_save_current_loop(self, event=None):
        """💾 Sauvegarde rapide (Ctrl+S) de la boucle AB courante dans saved_loops + fichier JSON."""
        if not hasattr(self, "current_loop") or not isinstance(self.current_loop, LoopData):
            Brint("[QUICK SAVE ERROR] Aucun current_loop valide")
            self.console.config(text="❌ Aucune boucle active à sauvegarder")
            return

        target_name = self.current_loop.name
        updated = False

        # Synchronize confirmed hits context before exporting
        self.current_loop.confirmed_hit_context = {
            "timestamps": sorted(getattr(self, "persistent_validated_hit_timestamps", [])),
            "grid_mode": getattr(self, "subdivision_mode", None),
        }
        self.current_loop.hit_timings = self.get_current_hit_timings()
        self.current_loop.hit_timestamps = self.get_current_hit_timestamps()

        # ✅ Ajouter les subdivisions rouges détectées
        self.current_loop.confirmed_red_subdivisions = getattr(self, "confirmed_red_subdivisions", {})

        for i, loop in enumerate(self.saved_loops):
            if loop["name"] == target_name:
                Brint(f"[SAVE DEBUG] current_loop.tempo_bpm = {getattr(self.current_loop, 'tempo_bpm', '❌ None')}")

                self.saved_loops[i] = self.current_loop.to_dict()
                Brint(f"[SAVE DEBUG] Boucle après to_dict() → {self.current_loop.to_dict()}")

                updated = True
                Brint(f"[QUICK SAVE] ♻ Boucle '{target_name}' mise à jour dans saved_loops")
                break

        if not updated:
            self.saved_loops.append(self.current_loop.to_dict())
            Brint(f"[QUICK SAVE] ➕ Boucle '{target_name}' ajoutée à saved_loops")

        self.save_loops_to_file()
        self.console.config(text=f"💾 Boucle '{target_name}' sauvegardée ({'maj' if updated else 'nouvelle'})")

    def reload_current_loop(self, event=None):
        """Reload the current loop from saved_loops (Shift+S)."""
        if not hasattr(self, "current_loop") or not isinstance(self.current_loop, LoopData):
            Brint("[RELOAD] ❌ Aucun current_loop valide")
            self.log_to_console("⚠️ Aucune boucle active à recharger")
            return

        target_name = self.current_loop.name
        for i, loop in enumerate(self.saved_loops):
            if loop.get("name") == target_name:
                Brint(f"[RELOAD] 🔄 Boucle trouvée : {target_name} (index {i})")

                self.load_saved_loop(i)

                # ✅ Recharger les subdivisions rouges
                red = loop.get("confirmed_red_subdivisions", {})
                self.confirmed_red_subdivisions = red
                Brint(f"[RELOAD] ✅ Red hits restaurés : {len(red)} subdivisions")

                self.log_to_console(f"🔄 Boucle '{target_name}' rechargée")
                return

        Brint(f"[RELOAD] ❌ Boucle '{target_name}' introuvable dans saved_loops")
        self.log_to_console(f"⚠️ Boucle '{target_name}' non trouvée")

        

    def hms(self, ms):
        original_value = ms  # pour debug

        try:
            if isinstance(ms, str):
                ms = float(ms.strip())
            elif not isinstance(ms, (int, float)):
                raise TypeError(f"Type inattendu: {type(ms)}")

            ms_total = int(ms)
            s_total = ms_total // 1000
            ms_remainder = ms_total % 1000

            h = s_total // 3600
            m = (s_total % 3600) // 60
            s = s_total % 60
            d = ms_remainder // 100  # affiche les dixièmes

            return f"{h}:{m:02}:{s:02}.{d}"

        except Exception as e:
            Brint(f"[WARNING] hms() → Impossible de convertir '{original_value}' en durée (ms). Erreur: {e}")
            return "N/A"

    def hms_from_seconds(self, seconds):
        original_value = seconds  # pour debug

        try:
            if isinstance(seconds, str):
                seconds = float(seconds.strip())
            elif not isinstance(seconds, (int, float)):
                raise TypeError(f"Type inattendu: {type(seconds)}")

            td = timedelta(seconds=seconds)
            h = int(td.total_seconds() // 3600)
            m = (td.seconds % 3600) // 60
            s = td.seconds % 60
            d = int(td.microseconds / 100000)
            return f"{h}:{m:02}:{s:02}.{d}"

        except Exception as e:
            Brint(f"[WARNING] hms_from_seconds() → Impossible de convertir '{original_value}' en durée (s). Erreur: {e}")
            return "N/A"
    def hms_to_seconds(hms):
        parts = list(map(float, hms.split(":")))
        return sum(t * 60**i for i, t in enumerate(reversed(parts)))

    def abph_stamp(self):
        """Return current A/B/playhead times in h:mm:ss.1 format."""
        from datetime import timedelta

        def fmt_ms(ms):
            if not isinstance(ms, (int, float)):
                return "N/A"
            td = timedelta(milliseconds=ms)
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            tenths = int((ms % 1000) / 100)  # dixièmes
            return f"{hours}:{minutes:02d}:{seconds:02d}.{tenths}"

        a = getattr(self, "loop_start", None)
        b = getattr(self, "loop_end", None)
        ph = getattr(self, "playhead_time", None)

        a_s = fmt_ms(a)
        b_s = fmt_ms(b)

        ph_s = fmt_ms(ph * 1000) if isinstance(ph, (int, float)) else "N/A"

        return f"A({a_s}) B({b_s}) PH({ph_s})"
    
    def compute_rhythm_grid_infos(self):
        Brint("[PRECOMPUTE] ▶️ Démarrage du calcul des subdivisions (X, label, state, is_playhead)")

        if not hasattr(self, "subdivision_counters"):
            Brint("[PRECOMPUTE] ℹ️ Init: subdivision_counters vide")
            self.subdivision_counters = {}

        if not hasattr(self, "subdiv_last_hit_pass"):
            Brint("[PRECOMPUTE] ℹ️ Init: subdiv_last_hit_pass vide")
            self.subdiv_last_hit_pass = {}

        if not hasattr(self, "grid_subdivs") or not self.grid_subdivs:
            Brint("[PRECOMPUTE] ⚠️ grid_subdivs vide — tentative de fallback ou recalcul nécessaire")
            self.debug_grid_subdivs("reset from compute_rhythm_grid_infos")

        if not self.grid_subdivs:
            Brint("[PRECOMPUTE ERROR] ❌ grid_subdivs toujours vide après tentative de recalcul — abandon.")
            self.precomputed_grid_infos = {}
            return {}

        canvas_width = self.grid_canvas.winfo_width()
        zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_end = zoom["zoom_end"]
        zoom_range = zoom["zoom_range"]
        x_params = dict(zoom=zoom, canvas_width=canvas_width)

        Brint(f"[PRECOMPUTE] 📏 canvas_width = {canvas_width}")
        Brint(f"[PRECOMPUTE] 🔍 zoom_start = {zoom_start:.1f} | zoom_end = {zoom_end:.1f} | zoom_range = {zoom_range:.1f}")


        subdivisions_per_beat = self.get_subdivisions_per_beat()


        Brint(f"[PRECOMPUTE] 🧮 subdivisions_per_beat = {subdivisions_per_beat} (mode = {self.subdivision_mode})")

        precomputed = {}
        playhead_x = getattr(self, 'playhead_canvas_x', -9999)

        if not hasattr(self, "subdiv_last_hit_time"):
            self.subdiv_last_hit_time = {}

        # Compute average subdivision interval for decay logic
        grid_times = [t for _, t in self.grid_subdivs]
        intervals = [t2 - t1 for t1, t2 in zip(grid_times[:-1], grid_times[1:])]
        self.avg_subdiv_interval_sec = sum(intervals) / len(intervals) if intervals else 0.5

        for idx, (i, t_subdiv_sec) in enumerate(self.grid_subdivs):
            x = self.time_sec_to_canvas_x(t_subdiv_sec, **x_params)

            state = self.subdivision_state.get(i, -1)
            is_playhead = abs(x - playhead_x) < 1

            if i < len(self.grid_labels):
                label = self.grid_labels[i]
            else:
                label = "-"

            precomputed[i] = {
                'x': x,
                'label': label,
                'state': state,
                'is_playhead': is_playhead,
                't_subdiv_sec': t_subdiv_sec
            }

            if idx < 5:
                Brint(f"[PRECOMPUTE] # Subdiv {i:>2} → t={t_subdiv_sec:.3f}s | x={x:>4.1f}px | label='{label}' | state={state} | [dyn] | playhead={is_playhead}")

        self.precomputed_grid_infos = precomputed
        Brint(f"[PRECOMPUTE] ✅ Calcul terminé : {len(precomputed)} subdivisions.")
        return precomputed
 
    def evaluate_subdivision_states(self):
        subdiv_interval = getattr(self, "avg_subdiv_interval_sec", 0.5)
        now_abs = None
        if getattr(self, "loop_duration_s", None) is not None:
            now_abs = self.loop_pass_count * self.loop_duration_s

        for i in self.grid_subdivs:

            idx = i[0]
            last_hit_loop = self.subdiv_last_hit_loop.get(idx, -1)
            state = self.subdivision_state.get(idx, -1)
            hit_count = self.subdivision_counters.get(idx, 0)
            last_hit_time = self.subdiv_last_hit_time.get(idx)


            if last_hit_loop == self.loop_pass_count - 1:
                # Si déjà orange -> passe en rouge validé
                if state == 1 and hit_count >= 3:

                    self.subdivision_state[idx] = 2
                    promoted_subdiv_idx = idx

                    Brint(f"[VALIDATED] Subdiv {promoted_subdiv_idx} passe en ROUGE (confirmée)")
                    # Add logic to store the original hit timestamp
                    if hasattr(self, "precomputed_grid_infos") and self.precomputed_grid_infos and \
                       hasattr(self, "user_hit_timestamps") and self.user_hit_timestamps:
                        current_grid_times_map = {idx: info['t_subdiv_sec'] for idx, info in self.precomputed_grid_infos.items()}
                        if current_grid_times_map:
                            grid_times_list = sorted(current_grid_times_map.values())
                            intervals = [t2 - t1 for t1, t2 in zip(grid_times_list[:-1], grid_times_list[1:])]
                            avg_interval_sec = sum(intervals) / len(intervals) if intervals else 0.5
                            # Wider window: half of the average subdivision interval
                            tolerance = avg_interval_sec / 2.0
                            Brint(f"[HIT WINDOW] ℹ️ Tolerance set to {tolerance:.3f}s (1/2 of {avg_interval_sec:.3f}s)")

                            loop_duration_s = None
                            if (
                                hasattr(self, "loop_end")
                                and hasattr(self, "loop_start")
                                and self.loop_end is not None
                                and self.loop_start is not None
                            ):
                                loop_duration_s = (
                                    self.loop_end - self.loop_start
                                ) / 1000.0

                            for t_hit, pass_count in self.user_hit_timestamps:
                                if pass_count == self.loop_pass_count - 1:  # Hit from the pass that just confirmed validation
                                    t_norm = (
                                        t_hit - pass_count * loop_duration_s
                                        if loop_duration_s is not None
                                        else t_hit
                                    )
                                    matched_idx_for_t_hit = None
                                    min_delta_for_t_hit = float('inf')
                                    for current_sub_idx, current_sub_t_sec in current_grid_times_map.items():
                                        delta = abs(current_sub_t_sec - t_norm)
                                        if delta < min_delta_for_t_hit:
                                            min_delta_for_t_hit = delta
                                            matched_idx_for_t_hit = current_sub_idx

                                    if matched_idx_for_t_hit == promoted_subdiv_idx and min_delta_for_t_hit <= tolerance:
                                        # self.persistent_validated_hit_timestamps.add(t_hit)
                                        # Brint(
                                            # passf"[PERSIST_HIT_ADD] Added {t_hit:.3f}s to persistent_validated_hit_timestamps for validated subdiv {promoted_subdiv_idx}"
                                        # )
                                        pass
                                else:
                                    Brint("[PERSIST_HIT_ADD] current_grid_times_map is empty, cannot associate timestamp.")
                        else:
                            Brint("[PERSIST_HIT_ADD] Missing precomputed_grid_infos or user_hit_timestamps, cannot associate timestamp.")
                    self.on_subdiv_validated(promoted_subdiv_idx)

                # Sinon devient orange pré-validée
                elif state == 0 and hit_count >= 2:

                    self.subdivision_state[idx] = 1
                    Brint(f"[PRE-VALIDATE] Subdiv {idx} passe en ORANGE")

            else:
                decay_threshold = None
                if now_abs is not None and last_hit_time is not None:
                    decay_threshold = now_abs - last_hit_time

                if (
                    decay_threshold is not None
                    and decay_threshold > self.loop_duration_s + subdiv_interval
                ):
                    if state == 1:
                        self.subdivision_state[idx] = 0
                        Brint(f"[DECAY] Subdiv {idx} ORANGE → GRIS")
                    elif state == 0:
                        self.subdivision_state[idx] = -1
                        Brint(f"[DECAY] Subdiv {idx} GRIS → AUCUN")
                    self.subdivision_counters[idx] = 0
                    if idx in self.subdiv_last_hit_loop:
                        del self.subdiv_last_hit_loop[idx]

        # ⚡ Optionnel : clean les entrées obsolètes
        # self.subdiv_last_hit_loop = {k: v for k, v in self.subdiv_last_hit_loop.items() if v >= self.loop_pass_count - 1}
    
    def sanitize_raw_hit_memory(self):
        """Nettoie raw_hit_memory en ne conservant que les tuples (float, int) valides."""
        if not hasattr(self, "raw_hit_memory"):
            self.raw_hit_memory = {}
            return

        for idx in list(self.raw_hit_memory.keys()):
            hits = self.raw_hit_memory[idx]
            cleaned = [
                (t, lp) for h in hits
                if isinstance(h, tuple) and len(h) == 2
                for (t, lp) in [h]
                if isinstance(t, (int, float)) and isinstance(lp, int)
            ]
            if cleaned:
                self.raw_hit_memory[idx] = cleaned
            else:
                del self.raw_hit_memory[idx]  # supprime les vides


    def prune_old_hit_memory(self):
        """Prune raw_hit_memory to keep hits from the last three loop passes."""
        if not hasattr(self, "raw_hit_memory"):
            return

        cutoff = max(0, self.loop_pass_count - 2)
        Brint(f"[NHIT] prune_old_hit_memory(cutoff={cutoff})")

        for idx in list(self.raw_hit_memory.keys()):
            hits = [
                (t, lp)
                for (t, lp) in self.raw_hit_memory.get(idx, [])
                if isinstance(lp, int) and lp >= cutoff
            ]
            if hits:
                self.raw_hit_memory[idx] = hits
            else:
                del self.raw_hit_memory[idx]

        if hasattr(self, "user_hit_timestamps"):
            self.user_hit_timestamps = [
                (t, lp) for (t, lp) in self.user_hit_timestamps if lp >= cutoff
            ]

    
    
    def reset_syllabic_grid_hits(self):
        if not hasattr(self, "persistent_validated_hit_timestamps"):
            self.persistent_validated_hit_timestamps = {}

        self.persistent_validated_hit_timestamps.clear()  # Clear persistent validated timestamps

        if hasattr(self, "confirmed_red_subdivisions"):
            self.confirmed_red_subdivisions.clear()

        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}
        else:
            self.subdivision_state.clear()

        if hasattr(self, "raw_hit_memory"):
            self.raw_hit_memory.clear()

        Brint("[NHIT] ✅ reset_syllabic_grid_hits() completed — all hit memory cleared.")





    
        if not hasattr(self, "grid_subdivs") or not self.grid_subdivs:
            Brint("[RESET SYLLABIC] Aucune grille active, rien à reset.")
            return

        if not hasattr(self, "subdivision_counters"):
            self.subdivision_counters = {}
        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}

        self.subdivision_counters.clear()
        self.subdivision_state.clear()
        self.subdiv_last_hit_loop = {}
        self.subdiv_last_hit_time = {}
        self.persistent_validated_hit_timestamps.clear() # Clear persistent validated timestamps
        
        for i, t_subdiv_ms in self.grid_subdivs: # Ensure this uses the correct structure of grid_subdivs
            idx_to_clear = i if isinstance(i, int) else i[0] # Adapt if grid_subdivs is list of tuples
            self.subdivision_counters[idx_to_clear] = 0
            self.subdivision_state[idx_to_clear] = -1
            self.subdiv_last_hit_loop[idx_to_clear] = -1

        # Supprimer les frappes dynamiques
        self.user_hit_timestamps = []

        # Supprimer les éléments affichés sur le canvas
        self.grid_canvas.delete("syllabic_label")
        self.grid_canvas.delete("syllabic_hit")

        Brint(f"[RESET SYLLABIC] Reset complet effectué : {len(self.grid_subdivs)} subdivisions remises à zéro (counters, states, timestamps, and persistent validated timestamps).")

        # Redessiner grille sans marques
        if hasattr(self, "draw_syllabic_grid_heatmap"):
            try:
                self.draw_syllabic_grid_heatmap()
            except AttributeError:
                pass

    # === New Hit Management API ===
    def record_user_hit(self, hit_time_ms):
        Brint(f"[NHIT] Hit registered at {self.hms(hit_time_ms)} | {self.abph_stamp()}")
        if not hasattr(self, "current_loop") or self.current_loop is None:
            return

        if not hasattr(self, "raw_hit_memory"):
            self.raw_hit_memory = {}  # idx → List[(timestamp_ms, loop_id)]

        # Ensure we have a list to store raw hit timestamps in seconds for drawing
        if not hasattr(self, "user_hit_timestamps"):
            self.user_hit_timestamps = []

        grid_sec = getattr(self, "grid_times", [])
        if not grid_sec:
            return
        grid_ms = [t * 1000 for t in grid_sec]
        interval = grid_ms[1] - grid_ms[0] if len(grid_ms) > 1 else 0

        if interval and getattr(self, "loop_start", None) is not None and getattr(self, "loop_end", None) is not None:
            loop_start_ms = self.loop_start
            loop_end_ms = self.loop_end
            if hit_time_ms < loop_start_ms - interval or hit_time_ms > loop_end_ms + interval:
                Brint(
                    f"[NHIT] Hit ignored (out of range) {self.hms(hit_time_ms)} | {self.abph_stamp()}"
                )
                return

        # Find closest subdivision
        idx = min(range(len(grid_ms)), key=lambda i: abs(grid_ms[i] - hit_time_ms))

        loop_id = self.loop_pass_count  # boucle logique actuelle
        self.raw_hit_memory.setdefault(idx, [])
        if loop_id in [lp for _, lp in self.raw_hit_memory[idx]]:
            Brint(f"[NHIT] Ignored duplicate hit on subdiv {idx} for loop {loop_id}")
            return

        self.raw_hit_memory[idx].append((hit_time_ms, loop_id))
        self.raw_hit_memory[idx] = self.raw_hit_memory[idx][-5:]
        Brint(
            f"[NHIT] raw_hit_memory[{idx}] += {self.hms(hit_time_ms)} | {self.abph_stamp()}"
        )

        if not hasattr(self, "subdiv_last_hit_time"):
            self.subdiv_last_hit_time = {}
        self.subdiv_last_hit_time[idx] = hit_time_ms

        # Record hit for matching and drawing routines (seconds, loop_id)
        if len(self.user_hit_timestamps) >= 200:
            Brint("[NHIT] Max hits reached, clear hits to resume")
            try:
                self.log_to_console("⚠️ Max hits reached. Clear hits to resume")
            except Exception:
                pass
        else:
            self.user_hit_timestamps.append((hit_time_ms / 1000.0, loop_id))

        self.update_subdivision_states()
        

        
    def update_subdivision_states(self):
        Brint(f"[NHIT] 🔄 update_subdivision_states() called | loop_pass_count = {self.loop_pass_count}")

        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}
        else:
            self.subdivision_state.clear()

        # Preserve existing red subdivisions
        if hasattr(self, "confirmed_red_subdivisions"):
            for ridx in self.confirmed_red_subdivisions.keys():
                self.subdivision_state[ridx] = 3

        for idx, hits in self.raw_hit_memory.items():
            if self.subdivision_state.get(idx) == 3:
                # Skip updates for persistent red subdivisions
                continue
            valid_hits = [
                (t, lp)
                for (t, lp) in hits
                if isinstance(t, (int, float)) and isinstance(lp, int)
            ]
            if not valid_hits:
                continue

            loop_ids = sorted(set(lp for _, lp in valid_hits))

            # Red state is reached when hits occur in three consecutive loop passes
            if len(loop_ids) >= 3 and loop_ids[-3:] == list(range(loop_ids[-3], loop_ids[-3] + 3)):
                self.subdivision_state[idx] = 3
                self.confirmed_red_subdivisions[idx] = [t for (t, _) in valid_hits[-3:]]
                Brint(f"[NHIT] Subdiv {idx} → RED (3) | loops = {loop_ids[-3:]}")
            elif len(loop_ids) >= 2 and loop_ids[-2:] == list(range(loop_ids[-2], loop_ids[-2] + 2)):
                self.subdivision_state[idx] = 2
                Brint(f"[NHIT] Subdiv {idx} → ORANGE (2) | loops = {loop_ids[-2:]}")
            else:
                self.subdivision_state[idx] = 1
                Brint(f"[NHIT] Subdiv {idx} → GRIS FONCÉ (1) | loops = {loop_ids}")

        # Prune old hits after computing state
        self.prune_old_hit_memory()

    def decay_subdivision_states(self):
        if self.loop_start is None or self.loop_end is None:
            return

        if not hasattr(self, "subdiv_last_hit_time"):
            self.subdiv_last_hit_time = {}
        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}

        loop_duration = self.loop_end - self.loop_start
        subdiv_interval = getattr(self, "avg_subdiv_interval_sec", 0.5) * 1000
        now = self.loop_start + self.loop_pass_count * loop_duration

        for idx, state in list(self.subdivision_state.items()):
            if state in (1, 2):
                last_hit_time = self.subdiv_last_hit_time.get(idx)
                if last_hit_time is None:
                    continue
                if now - last_hit_time > loop_duration + subdiv_interval:
                    prev = state
                    new_state = state - 1
                    self.subdivision_state[idx] = new_state
                    Brint(f"[NHIT] Subdiv {idx} decayed from state {prev} to {new_state}")
                    # purge old hit info so this subdivision isn't promoted
                    if hasattr(self, "raw_hit_memory") and idx in self.raw_hit_memory:
                        del self.raw_hit_memory[idx]
                    self.subdiv_last_hit_time.pop(idx, None)
                    if hasattr(self, "subdiv_last_hit_loop") and idx in self.subdiv_last_hit_loop:
                        del self.subdiv_last_hit_loop[idx]
                    if hasattr(self, "subdivision_counters") and idx in self.subdivision_counters:
                        self.subdivision_counters[idx] = 0



    






    def offset_red_subdivisions(self, direction):
        """Shift all red subdivision hits up/down by one subdivision unit."""
        bpm = getattr(self, "tempo_bpm", 0)
        if bpm <= 0 or not getattr(self, "grid_times", None):
            return
        interval = (60.0 / bpm / self.get_subdivisions_per_beat()) * 1000  # in ms

        new_reds = {}
        for idx, timestamps in self.confirmed_red_subdivisions.items():
            new_ts = [t + direction * interval for t in timestamps]
            new_reds[idx] = new_ts
            Brint(f"[NHIT] Offset subdiv {idx}: {timestamps} → {new_ts}")
        self.confirmed_red_subdivisions = new_reds

    def reset_red_hits(self):
        self.confirmed_red_subdivisions = {}
        self.raw_hit_memory = {}
        Brint("[NHIT] All red hits reset")

    def get_subdivision_state(self, idx):
        return self.subdivision_state.get(idx, 0)
    
    def associate_hits_to_subdivisions(self):
        """
        Associe tous les hits rouges (confirmés) à la subdivision la plus proche
        selon la grille actuelle. Écrase les anciennes associations.
        """
        if not getattr(self, "confirmed_red_subdivisions", None):
            self.confirmed_red_subdivisions = {}
            return self.confirmed_red_subdivisions

        grid_sec = getattr(self, "grid_times", [])
        if not grid_sec:
            return self.confirmed_red_subdivisions

        grid_ms = [t * 1000 for t in grid_sec]
        if not grid_ms:
            Brint("[NHIT] ⚠️ associate_hits_to_subdivisions() — grid_ms est vide, skip association")
            return {}

        if len(grid_ms) < 2:
            return self.confirmed_red_subdivisions

        reassociated = {}
        for hit_list in self.confirmed_red_subdivisions.values():
            for raw_t in hit_list:
                t = raw_t[0] if isinstance(raw_t, tuple) else raw_t
                idx = min(range(len(grid_ms)), key=lambda i: abs(grid_ms[i] - t))
                if idx not in reassociated:
                    reassociated[idx] = []
                reassociated[idx].append(t)
                Brint(
                    f"[RED REASSOC] Hit {t:.1f}ms reassocié à subdiv {idx} (grille @ {grid_ms[idx]:.1f}ms)"
                )

        self.confirmed_red_subdivisions = reassociated
        Brint(f"[RED REASSOC] ✅ {len(reassociated)} subdivisions rouges mises à jour")
        return self.confirmed_red_subdivisions












    def offset_all_hit_timestamps(self, direction):
        """Shift all hit timestamps by one subdivision forward or backward."""
        bpm = getattr(self, "tempo_bpm", 0)
        if bpm <= 0:
            Brint("[OFFSET HITS] tempo_bpm manquant – opération annulée")
            return
        interval = 60.0 / bpm / self.get_subdivisions_per_beat()
        # Keep track of which subdivisions were confirmed (state = 3) prior to the shift

        prev_confirmed = {
            idx for idx, state in getattr(self, "subdivision_state", {}).items() if state == 2
        }
        force_state_indices = []
        if prev_confirmed and getattr(self, "persistent_validated_hit_timestamps", None):
            # Use the ordered grid_times list so indices correspond to subdivision_state keys
            grid_times = getattr(self, "grid_times", [])
            if not grid_times and getattr(self, "precomputed_grid_infos", None):
                grid_times = [
                    info["t_subdiv_sec"] for _, info in sorted(self.precomputed_grid_infos.items())
                ]

            for t in self.get_all_red_hit_timestamps():
                idx_old = self.current_loop.timestamp_to_subdiv_index(t, grid_times)
                if idx_old in prev_confirmed:
                    t_new = t + direction * interval
                    idx_new = self.current_loop.timestamp_to_subdiv_index(t_new, grid_times)
                    if idx_new is not None:
                        force_state_indices.append(idx_new)
        if hasattr(self, "user_hit_timestamps"):
            self.user_hit_timestamps = [
                (t + direction * interval, lp) for t, lp in self.user_hit_timestamps
            ]
        if hasattr(self, "persistent_validated_hit_timestamps"):
            self.confirmed_red_subdivisions = {
                idx: [t + direction * interval for t in hits]
                for idx, hits in self.confirmed_red_subdivisions.items()
            }
        # After shifting, remap persistent hits so that red subdivisions follow
        self.remap_persistent_validated_hits()
        for idx in force_state_indices:
            self.subdivision_state[idx] = 2
            Brint(f"[OFFSET HITS] Forced state=2 on subdiv {idx} after offset")
        if hasattr(self, "refresh_chord_editor"):
            try:
                self.refresh_chord_editor()
            except AttributeError:
                pass
        Brint(
            f"[OFFSET HITS] Décalage de {direction:+d} subdiv → Δ={direction*interval:.3f}s"
        )
        if hasattr(self, "draw_syllabic_grid_heatmap"):
            try:
                self.draw_syllabic_grid_heatmap()
            except AttributeError:
                pass

    def shift_all_hit_timestamps(self, delta_sec):
        """Shift all hit timestamps by an arbitrary time delta."""
        if delta_sec == 0:
            return
        if hasattr(self, "user_hit_timestamps"):
            self.user_hit_timestamps = [
                (t + delta_sec, lp) for t, lp in self.user_hit_timestamps
            ]
        self.confirmed_red_subdivisions = {
            idx: [t + delta_sec * 1000 for t in hits]
            for idx, hits in self.confirmed_red_subdivisions.items()
        }

        self.remap_persistent_validated_hits()
    
    def time_ms_to_canvas_x(self, t_ms):
        zoom_ratio = self.loop_zoom_ratio or 1.0
        loop_width = self.loop_end - self.loop_start
        zoom_width = int(loop_width / zoom_ratio)

        zoom_start = self.loop_start
        zoom_range = zoom_width

        canvas_width = self.grid_canvas.winfo_width()
        return int((t_ms - zoom_start) / zoom_range * canvas_width)
    
    
    def get_subdiv_label(self, i):
        if 0 <= i < len(self.grid_labels):
            return self.grid_labels[i]
        else:
            return "?"


    def get_all_red_hit_timestamps(self):
        """Renvoie tous les timestamps (en secondes) des subdivisions rouges."""
        if not hasattr(self, "confirmed_red_subdivisions"):
            return set()
        timestamps = set()
        for hits in self.confirmed_red_subdivisions.values():
            for raw_t in hits:
                t = raw_t[0] if isinstance(raw_t, tuple) else raw_t
                timestamps.add(t / 1000.0)
        return timestamps


    def toggle_subdiv_state_manual(self, subdiv_index, t_ms):
        """
        Active ou désactive manuellement une subdivision rouge.
        Si déjà rouge, elle est supprimée ; sinon, ajoutée avec le timestamp donné.
        """
        if not hasattr(self, "confirmed_red_subdivisions"):
            self.confirmed_red_subdivisions = {}
        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}

        t_ms = int(t_ms)  # sécurité
        t_list = self.confirmed_red_subdivisions.get(subdiv_index, [])

        if subdiv_index in self.confirmed_red_subdivisions:
            del self.confirmed_red_subdivisions[subdiv_index]
            self.subdivision_state[subdiv_index] = 0
            if hasattr(self, "raw_hit_memory") and subdiv_index in self.raw_hit_memory:
                del self.raw_hit_memory[subdiv_index]
            Brint(f"[TOGGLE] Subdiv {subdiv_index} reset (removed {t_ms} ms)")
        else:
            self.confirmed_red_subdivisions[subdiv_index] = [t_ms] * 3
            self.subdivision_state[subdiv_index] = 3
            Brint(f"[TOGGLE] Subdiv {subdiv_index} set RED (added {t_ms} ms)")

        if hasattr(self, "draw_rhythm_grid_canvas"):
            self.draw_rhythm_grid_canvas()

    def apply_all_chords(self, entry_vars, popup):
        Brint("[DEBUG] ✅ Application des modifications")
        self.current_loop.chords = []
        for (bp, chord_var) in entry_vars:
            chord_name = normalize_chord_name(chord_var.get())
            if chord_name:
                self.current_loop.update_chord_at_beat(bp, chord_name)
        self.current_loop.sort_chords()

        # Export propre vers dict
        updated_loop_dict = loopdata_to_dict(self.current_loop)

        # Remplacement ou ajout dans self.saved_loops
        found = False
        for i, loop in enumerate(self.saved_loops):
            if loop.get("name", "") == updated_loop_dict["name"]:
                self.saved_loops[i] = updated_loop_dict
                Brint(f"[INFO] Boucle '{updated_loop_dict['name']}' mise à jour dans saved_loops.")
                found = True
                break

        if not found:
            self.saved_loops.append(updated_loop_dict)
            Brint(f"[INFO] Nouvelle boucle '{updated_loop_dict['name']}' ajoutée dans saved_loops.")

        # Sauvegarde sur disque
        self.save_loops_to_file()
        self.refresh_note_display()
        Brint(f"[DEBUG] 🎼 Boucle '{self.current_loop.name}' sauvegardée et interface mise à jour")
        popup.destroy()


    
    
    def degree_from_chord(self, chord, key):
        degrees = {
            key: ["I", "II", "III", "IV", "V", "VI", "VII"]
            for key in [
                "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb",
                "G", "G#", "Ab", "A", "A#", "Bb", "B"
            ]
        }
        # Simplification extrême pour l'exemple (à remplacer par une vraie logique)
        if not chord:
            return ""
        # Retourne "?" si key inconnue
        try:
            return degrees[key][0]  # TEMP LOGIC : à remplacer par vraie analyse harmonique
        except:
            return "?"

    
    
    def invalidate_jump_estimators(self):
        if hasattr(self, 'last_jump_target_ms'):
            self.last_jump_target_ms = None
        if hasattr(self, 'last_jump_timestamps'):
            self.last_jump_timestamps.clear()
        Brint("[FORCED RESET] Jump estimators invalidés après update boucle")
    def validate_loop_data(self, loop):
        """Valide qu'une boucle contient au minimum loop_start et loop_end valides (ms > 0 et end > start)."""
        if not isinstance(loop, dict):
            return False, "Données de boucle invalides (pas un dict)"
        if loop.get("loop_start") is None or loop.get("loop_end") is None:
            return False, "Loop start ou end manquant"
        if not isinstance(loop["loop_start"], (int, float)) or not isinstance(loop["loop_end"], (int, float)):
            return False, "Loop start ou end non numériques"
        if loop["loop_start"] >= loop["loop_end"]:
            return False, f"Loop start >= loop end ({loop['loop_start']} >= {loop['loop_end']})"

        ctx = loop.get("confirmed_hit_context")
        if ctx is not None:
            if not isinstance(ctx, dict):
                return False, "confirmed_hit_context invalide"
            if "timestamps" in ctx and not isinstance(ctx["timestamps"], list):
                return False, "timestamps doit être une liste"
            if "grid_mode" in ctx and ctx["grid_mode"] is not None and not isinstance(ctx["grid_mode"], str):
                return False, "grid_mode doit être une chaîne ou None"
        return True, None

    
    def handle_screen_zoom_keypress(self, event):
        # Debug toujours visible
        Brint(f"[KEY DEBUG] keysym='{event.keysym}' | keycode={event.keycode} | char='{event.char}'")

        # PAN via pavé numérique (keycode fiable Windows)
        if event.keycode == 100 or event.keysym == 'KP_Left':
            self.pan_left()
        elif event.keycode == 102 or event.keysym == 'KP_Right':
            self.pan_right()
        elif event.keycode == 104 or event.keysym == 'KP_Up':
            self.pan_up()
        elif event.keycode == 98 or event.keysym == 'KP_Down':
            self.pan_down()

        # ZOOM via pavé numérique (keycode fiable)
        elif event.keycode == 105 or event.keysym == 'KP_Prior':  # Numpad 9 (PgUp)
            self.zoom_in()
        elif event.keycode == 103 or event.keysym == 'KP_Home':   # Numpad 7 (Home)
            self.zoom_out()
            
        elif event.keycode == 101: self.reset_or_revert_zoom()    
        elif event.keycode == 96: self.on_user_hit()   
        
    def debug_keypress(self, event):
        Brint(f"[KEY DEBUG] keysym='{event.keysym}' | keycode={event.keycode} | char='{event.char}'")
    #config player zoom
    
    
    



    def on_zoom_button_click(self):
        self.open_zoom_mode()  # Active le mode zoom contextuel + clavier
        # Ensuite, afficher le menu zoom sous la souris, centré sur le bouton
        x = self.zoom_menu_button.winfo_rootx()
        y = self.zoom_menu_button.winfo_rooty() + self.zoom_menu_button.winfo_height()
        self.zoom_menu.post(x, y)

    
    def open_zoom_mode(self):
        self.in_zoom_mode = True
        Brint("[ZOOM MODE] Entrée en mode Zoom. Utilise +, -, ←, →")
        # Optionnel : popup ou toast
        self.show_console_message("Mode Zoom actif : +, -, ←, →. Esc pour quitter.")

    def close_zoom_mode(self):
        self.in_zoom_mode = False
        self.save_current_zoom()
        Brint("[ZOOM MODE] Sortie de mode Zoom et sauvegarde.")
        self.show_console_message("Zoom sauvegardé.")
  
    def handle_keypress(self, event):
        if self.in_zoom_mode:
            if event.keysym == "plus" or event.char == '+':
                self.zoom_in()
            elif event.keysym == "minus" or event.char == '-':
                self.zoom_out()
            elif event.keysym == "Left":
                self.pan_left()
            elif event.keysym == "Right":
                self.pan_right()
            elif event.keysym == "Escape":
                self.close_zoom_mode()
        else:
            # Ton comportement normal ici
            pass  # Ou route vers autre logique globale

    
    def load_player_settings(self):
        settings_file = os.path.join(os.path.dirname(__file__), "player_settings.json")
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as f:
                    return json.load(f)
            except:
                Brint("[ERROR] Impossible de lire player_settings.json")
                return {}
        return {}

    def save_player_settings(self, data):
        settings_file = os.path.join(os.path.dirname(__file__), "player_settings.json")
        try:
            with open(settings_file, "w") as f:
                json.dump(data, f, indent=4)
        except:
            Brint("[ERROR] Impossible d'écrire player_settings.json")
    def build_screen_zoom_menu(self, zoom_menu):
        zoom_menu.add_command(label="Sauvegarder Zoom", command=self.save_screen_zoom_prefs)
        self.reset_zoom_label_text = "Reset Zoom"
        zoom_menu.add_command(label=self.reset_zoom_label_text, command=self.reset_or_revert_zoom)
        self.reset_zoom_menu_index = zoom_menu.index("end")
        zoom_menu.add_separator()
        zoom_menu.add_command(label="🔍+ Zoom avant", command=self.zoom_in)
        zoom_menu.add_command(label="🔎− Zoom arrière", command=self.zoom_out)
        zoom_menu.add_command(label="⬅️ Déplacer à gauche", command=self.pan_left)
        zoom_menu.add_command(label="➡️ Déplacer à droite", command=self.pan_right)
        zoom_menu.add_separator()
        zoom_menu.add_command(label="🔄 Réinitialiser", command=self.reset_crop)

        # Bindings activés/désactivés uniquement quand menu ouvert
        zoom_menu.bind("<Map>", lambda e: self.enable_zoom_keyboard_controls())
        zoom_menu.bind("<Unmap>", lambda e: self.disable_zoom_keyboard_controls())


        def enable_zoom_keyboard_controls(self):
            self.root.bind("+", lambda e: self.zoom_in())
            self.root.bind("-", lambda e: self.zoom_out())
            self.root.bind("<Left>", lambda e: self.pan_left())
            self.root.bind("<Right>", lambda e: self.pan_right())
            Brint("[ZOOM MODE] Raccourcis activés")

        def disable_zoom_keyboard_controls(self):
            self.root.unbind("+")
            self.root.unbind("-")
            self.root.unbind("<Left>")
            self.root.unbind("<Right>")
            Brint("[ZOOM MODE] Raccourcis désactivés")




    def save_current_zoom(self):
        data = self.load_player_settings()
        data["zoom_ratio"] = self.zoom_loop_ratio
        self.save_player_settings(data)
        Brint(f"[SAVE] Zoom sauvegardé à {self.zoom_loop_ratio:.2f}")

    def reset_or_revert_zoom(self):
        if not hasattr(self, 'zoom_last_saved'):
            # On stocke le zoom courant pour revenir plus tard
            self.zoom_last_saved = (self.global_zoom_level, self.global_crop_x)
            self.reset_crop()
            Brint("[ZOOM] Reset → bouton devient Revert Zoom")
            self.zoom_menu.entryconfig(self.reset_zoom_menu_index, label="Revert Zoom")
        else:
            # On revient au zoom sauvegardé
            self.global_zoom_level, self.global_crop_x = self.zoom_last_saved
            self.apply_crop()
            Brint("[ZOOM] Revert → bouton redevient Reset Zoom")
            del self.zoom_last_saved
            self.zoom_menu.entryconfig(self.reset_zoom_menu_index, label="Reset Zoom")


    def on_screen_zoom_change(self, value):
        try:
            self.zoom_loop_ratio = float(value)
            Brint(f"[ZOOM] 🔍 Zoom boucle réglé sur {self.zoom_loop_ratio:.2f} (AB = {self.zoom_loop_ratio*100:.0f}% de la timeline)")
            self.draw_rhythm_grid_canvas()

            # Planifier un autosave après un délai (2s)
            if hasattr(self, '_pending_zoom_autosave'):
                self.root.after_cancel(self._pending_zoom_autosave)
            self._pending_zoom_autosave = self.root.after(2000, self.auto_save_zoom_after_change)
        except:
            Brint("[ERROR] Mauvaise valeur de zoom")

    def auto_save_zoom_after_change(self):
        self.save_current_zoom()
        Brint("[AUTO-SAVE] Zoom sauvegardé automatiquement après modification.")

    #jumps and smooth playhead
    
    def set_forced_jump(self, value, source="UNKNOWN"):
        old_value = getattr(self, 'in_forced_jump', False)
        if old_value == value:
            pass#LOOPJUMPBrint(f"[FORCED JUMP TRACKER] {source} a ignoré changement inutile : déjà {value}")
        else:
            self.in_forced_jump = value
            Brint(f"[FORCED JUMP TRACKER] {source} change in_forced_jump: {old_value} → {value}")
            
    def safe_jump_to_time(self, target_ms, source="UNKNOWN"):
        Brint(f"[PH JUMP] 🚀 {source} → jump à {int(target_ms)} ms demandé")

        self.player.set_time(int(target_ms))
        self.set_forced_jump(True, source=source)
        self.safe_update_playhead(target_ms, source)



    def safe_update_playhead(self, target_ms, source="UNKNOWN"):
        if self.in_local_loop_mode and source != "Loop interpolation":
            # Brint(f"[DRAW TRACKER BLOCKED] {source} bloqué car en loop locale.")
            Brint(f"[PH BLOCKED] {source} → update ignoré (loop locale active)")
            
            return
        self.playhead_time = target_ms / 1000.0
        Brint(f"[PH SET] {source} → playhead_time = {self.playhead_time:.3f}s ({int(target_ms)} ms)")
        self.update_playhead_by_time(target_ms)

    
    def build_loop_data(self, name):
        if not hasattr(self, "current_loop") or not isinstance(self.current_loop, LoopData):
            Brint("[ERROR] Aucun LoopData actif pour la sauvegarde")
            return {}

        loop_data = {
            "name": name,
            "loop_start": self.loop_start,
            "loop_end": self.loop_end,
            "master_note_list": self.current_loop.master_note_list,
            "chords": self.current_loop.chords,
            "tempo_bpm": self.current_loop.tempo_bpm,
            "key": self.current_loop.key,
            "mode": self.current_loop.mode,
            "loop_zoom_ratio": getattr(self, "loop_zoom_ratio", None),  # ✅ new field
            "confirmed_hit_context": {
                "timestamps": sorted(self.get_all_red_hit_timestamps()),
                "grid_mode": self.subdivision_mode,
            },
            "hit_timings": self.get_current_hit_timings(),
            "hit_timestamps": self.get_current_hit_timestamps(),
        }

        is_valid, reason = self.validate_loop_data(loop_data)
        if not is_valid:
            Brint(f"[ERROR] Tentative de sauvegarder une boucle invalide : {reason}")

        Brint(f"[DEBUG] Loop sauvegardée : {loop_data['loop_start']} → {loop_data['loop_end']}, "
              f"{len(loop_data['master_note_list'])} notes, "
              f"{len(loop_data['chords'])} accords (beat_position), "
              f"tempo = {loop_data['tempo_bpm']}, key = {loop_data['key']}, mode = {loop_data['mode']}")
        return loop_data

    def get_current_hit_timings(self):
        """Return timings (in sec) of red hits, normalized to current loop."""
        if not getattr(self, "confirmed_red_subdivisions", None):
            return []
        if self.loop_end is None or self.loop_start is None:
            return []

        loop_duration_s = (self.loop_end - self.loop_start) / 1000.0
        if loop_duration_s <= 0:
            return []

        red_hits = [t for hits in self.confirmed_red_subdivisions.values() for t in hits]
        timings = [(t / 1000.0) % loop_duration_s for t in red_hits]
        return sorted(timings)

    def get_current_hit_timestamps(self):
        """Return list of all red hit timestamps in ms."""
        if not getattr(self, "confirmed_red_subdivisions", None):
            return []
        return sorted(int(t) for hits in self.confirmed_red_subdivisions.values() for t in hits)

    
        
    def increase_tempo(self):
        new_bpm = round(self.tempo_bpm + 0.6)
        self.set_tempo_bpm(new_bpm, source="feather +")

    def decrease_tempo(self):
        new_bpm = round(self.tempo_bpm - 0.6)
        if new_bpm <= 0:
            new_bpm = 0.1  # pour éviter les valeurs négatives ou nulles
        self.set_tempo_bpm(new_bpm, source="feather -")

        
    def log_to_console(self, message):
        self.console.config(text=message)

    def open_audio_power_window(self):
        if not hasattr(self, 'current_path'):
            return


# codex/ajouter-fenêtre-de-visualisation-du-signal-audio

        if not hasattr(self, 'audio_power_data') or self.audio_power_data is None:
            self._compute_audio_power_data()
            if not hasattr(self, 'audio_power_data') or self.audio_power_data is None:
                return

        if hasattr(self, 'power_window') and self.power_window.winfo_exists():
            return

        self.power_window = tk.Toplevel(self.root)
        self.power_window.title('Audio Power')
        fig, ax = plt.subplots(figsize=(6, 3))
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=self.power_window)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        self._power_line, = ax.plot([], [])
        ax.set_ylim(0, max(self.audio_power_data[1]) * 1.1)
        ax.set_xlim(0, 10)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('RMS')

        def _update():
            if not self.power_window.winfo_exists():
                return
            current_sec = self.player.get_time() / 1000.0
            start = max(0, current_sec - 10)
            times, rms = self.audio_power_data
            mask = (times >= start) & (times <= current_sec)
            ax.set_xlim(start, current_sec if current_sec > start else start + 10)
            self._power_line.set_data(times[mask], rms[mask])
            canvas.draw()
            self.power_window.after(200, _update)

        _update()


# codex/ajouter-fenêtre-de-visualisation-du-signal-audio


    def _compute_audio_power_data(self):
        if not getattr(self, 'current_path', None):
            return
        try:
            y, sr = librosa.load(self.current_path, sr=None, mono=True)
            hop = 512
            rms = librosa.feature.rms(y=y, hop_length=hop)[0]
            times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
            self.audio_power_data = (times, rms)
            self.audio_power_max = float(rms.max()) if len(rms) else 0.0
        except Exception:
            self.audio_power_data = None
            self.audio_power_max = 0.0
        self.root.after(0, self.refresh_static_timeline_elements)

    def open_debug_flags_window(self):
        """Open a window with checkboxes to toggle DEBUG_FLAGS."""
        if getattr(self, 'flags_window', None) and self.flags_window.winfo_exists():
            self.flags_window.lift()
            return

        self.flags_window = tk.Toplevel(self.root)
        self.flags_window.title('Debug Flags')

        # Special handling for global BRINT flag with tri-state control
        options = ['None', 'False', 'True']
        var_brint = tk.StringVar(value=str(DEBUG_FLAGS.get('BRINT')))

        def update_brint(choice):
            if choice == 'None':
                DEBUG_FLAGS['BRINT'] = None
            elif choice == 'True':
                DEBUG_FLAGS['BRINT'] = True
            else:
                DEBUG_FLAGS['BRINT'] = False

        tk.Label(self.flags_window, text='BRINT').pack(anchor='w')
        tk.OptionMenu(self.flags_window, var_brint, *options, command=update_brint).pack(anchor='w')

        # Boolean flags
        self.debug_vars = {}
        for flag in sorted(k for k in DEBUG_FLAGS.keys() if k != 'BRINT'):
            var = tk.BooleanVar(value=bool(DEBUG_FLAGS[flag]))
            self.debug_vars[flag] = var

            def toggle(f=flag, v=var):
                DEBUG_FLAGS[f] = v.get()

            chk = tk.Checkbutton(self.flags_window, text=flag, variable=var, command=toggle)
            chk.pack(anchor='w')

    def apply_loop_zoom_ratio(self, ratio):
        """Apply the given zoom ratio to the loop and refresh display."""
        self.loop_zoom_ratio = ratio
        Brint(
            f"[ZOOM] 🔍 Zoom boucle réglé sur {self.loop_zoom_ratio:.2f} (AB = {int(self.loop_zoom_ratio * 100)}% de la timeline)"
        )

        if self.loop_start is not None and self.loop_end is not None and self.duration:
            loop_width_ms = max(float(MIN_ZOOM_RANGE_MS), self.loop_end - self.loop_start)
            center_ms = (self.loop_start + self.loop_end) / 2.0
            desired_ms = loop_width_ms / self.loop_zoom_ratio
            if self.loop_zoom_ratio > 1.0:
                desired_ms = max(float(MIN_ZOOM_RANGE_MS), desired_ms)
                desired_ms = min(desired_ms, loop_width_ms)
            zoom_start = max(0.0, center_ms - desired_ms / 2.0)
            zoom_end = min(self.duration, zoom_start + desired_ms)
            self.zoom_context = {
                "zoom_start": zoom_start,
                "zoom_end": zoom_end,
                "zoom_range": zoom_end - zoom_start,
            }

        self.refresh_static_timeline_elements()
        self.draw_rhythm_grid_canvas()

    def compute_ratio_for_4s(self):
        """Return the zoom ratio that shows approximately 4 seconds of the loop."""
        if self.loop_start is None or self.loop_end is None:
            return 1.0
        loop_width_ms = max(float(MIN_ZOOM_RANGE_MS), self.loop_end - self.loop_start)
        return loop_width_ms / float(MIN_ZOOM_RANGE_MS)

    def increase_loop_zoom(self):
        """Move the zoom slider up one step and trigger the change callback."""
        if not hasattr(self, "zoom_slider"):
            return
        try:
            max_idx = int(self.zoom_slider["to"])
        except Exception:
            max_idx = len(getattr(self, "zoom_levels", [])) - 1
        current = getattr(self.zoom_slider, "value", 0)
        new_idx = min(current + 1, max_idx)
        self.zoom_slider.set(new_idx)
        if hasattr(self, "on_loop_zoom_change"):
            try:
                self.on_loop_zoom_change(new_idx)
            except Exception:
                pass

    def decrease_loop_zoom(self):
        """Move the zoom slider down one step and trigger the change callback."""
        if not hasattr(self, "zoom_slider"):
            return
        try:
            min_idx = int(self.zoom_slider["from"])
        except Exception:
            min_idx = 0
        current = getattr(self.zoom_slider, "value", 0)
        new_idx = max(current - 1, min_idx)
        self.zoom_slider.set(new_idx)
        if hasattr(self, "on_loop_zoom_change"):
            try:
                self.on_loop_zoom_change(new_idx)
            except Exception:
                pass

    def on_zoom_ratio_change(self):
        val = self.zoom_ratio_var.get()
        if val == self.zoom_auto_code:
            ratio = self.compute_ratio_for_4s()
        else:
            ratio = float(val)
        self.apply_loop_zoom_ratio(ratio)


    

    def get_loop_zoom_range(self):
        if self.loop_start and self.loop_end:
            loop_width_sec = max(MIN_ZOOM_RANGE_MS / 1000.0, (self.loop_end - self.loop_start) / 1000.0)
            center_sec = (self.loop_start + self.loop_end) / 2000.0
            desired_sec = loop_width_sec / self.loop_zoom_ratio
            if self.loop_zoom_ratio > 1.0:
                desired_sec = max(MIN_ZOOM_RANGE_MS / 1000.0, desired_sec)
                desired_sec = min(desired_sec, loop_width_sec)
            zoom_start = max(0, center_sec - desired_sec / 2.0)
            zoom_end = min(self.duration / 1000.0, center_sec + desired_sec / 2.0)
            return zoom_start, zoom_end
        return 0, self.duration / 1000.0

    
    def invalidate_loop_name_if_modified(self):
        # Si les curseurs ont bougé depuis la loop sélectionnée, on invalide le nom
        if hasattr(self, "selected_loop_data"):
            ref = self.selected_loop_data
            if self.loop_start != ref.get("loop_start") or self.loop_end != ref.get("loop_end"):
                Brint("[TRACE] loop A/B modifiée manuellement → selected_loop_name effacé")
                self.selected_loop_name = None

   
    # === Centralized export logic ===
    def set_selected_loop_name(self, name, loop_start=None, loop_end=None, source="(non spécifié)"):
        a_ms = loop_start if loop_start is not None else "N/A"
        b_ms = loop_end if loop_end is not None else "N/A"
        # Brint(f"[TRACE] set_selected_loop_name = '{name}' (A={a_ms}ms, B={b_ms}ms) depuis {source}")
        Brint(f"[TRACE] set_selected_loop_name = '{name}' (A={self.hms(a_ms)}ms, B={self.hms(b_ms)}ms) depuis {source}")
        self.selected_loop_name = name

    def sanitize_filename(self, name):
        import re
        name = name.strip()
        name = name.replace(" ", "_")
        name = re.sub(r"[^a-zA-Z0-9_\\-]", "", name)
        return name
    def build_export_menu(self, parent):
        from tkinter import Toplevel, BooleanVar, Checkbutton, Button

        menu = Toplevel(parent)
        menu.title("Export Loop")

        # Variables liées aux options
        var_repeat = BooleanVar()
        var_video = BooleanVar()

        # Checkboxes d'options
        Checkbutton(menu, text="🔁 Export x10", variable=var_repeat).pack(anchor="w")
        Checkbutton(menu, text="🎬 Export as video", variable=var_video).pack(anchor="w")

        # Bouton pour export local
        Button(menu, text="💾 Save to HDD", command=lambda: (
            self.export_loop_to_file(
                repeat=var_repeat.get(),
                video=var_video.get(),
                destination='disk'
            ),
            menu.destroy()
        ), width=20).pack(pady=5)

        # Bouton pour export vers Google Drive
        Button(menu, text="☁️ Save to GDrive", command=lambda: (
            self.export_loop_to_file(
                repeat=var_repeat.get(),
                video=var_video.get(),
                destination='gdrive'
            ),
            menu.destroy()
        ), width=20).pack(pady=5)

        # Bouton pour uploader le .py sur GDrive
        # Button(menu, text="🟪 PY: Save .py to GDrive", command=lambda: (
            # self.upload_current_py_to_drive(),
            # menu.destroy()
        # ), width=25).pack(pady=5)
    def export_loop_to_file(self, repeat=False, video=False, destination='disk'):
        if not self.loop_start or not self.loop_end or not self.current_path:
            self.console.config(text="❌ Impossible d'exporter : informations de loop manquantes.")
            return
        # Nom de base du fichier (si boucle sauvegardée, sinon fallback)
        if not hasattr(self, "selected_loop_name") or not self.selected_loop_name:
            base = os.path.splitext(os.path.basename(self.current_path))[0]
            self.set_selected_loop_name(f"{self.sanitize_filename(base)}_loop", context="export fallback")

        raw_name = self.selected_loop_name
        base_name = self.sanitize_filename(raw_name)
        Brint(f"[EXPORT] selected_loop_name = {getattr(self, 'selected_loop_name', '❌ None')}")

        start_sec = self.loop_start / 1000.0
        duration_sec = (self.loop_end - self.loop_start) / 1000.0
        suffix = "_vid" if video else "_wav"
        suffix += "_x10" if repeat else "_x1"
        filename = f"{base_name}{suffix}.{ 'mp4' if video else 'wav' }"
        if destination == 'disk':
            filetypes = [("Fichiers MP4", "*.mp4")] if video else [("Fichiers WAV", "*.wav")]
            defaultext = ".mp4" if video else ".wav"
            output_path = filedialog.asksaveasfilename(
                defaultextension=defaultext,
                filetypes=filetypes,
                title="Sauvegarder la boucle A-B",
                initialfile=filename
            )

            
            if not output_path:
                return
        else:
            # destination == 'gdrive'
            media_base_name = os.path.splitext(os.path.basename(self.current_path))[0]
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, filename)

        if video:
            if repeat:
                # Export video segment to temp file
                tmp_clip = os.path.join(tempfile.gettempdir(), "loop_segment.mp4")
                cmd_extract = [
                    "ffmpeg", "-y",
                    "-ss", str(start_sec),
                    "-t", str(duration_sec),
                    "-i", self.current_path,
                    "-c", "copy",
                    tmp_clip
                ]
                subprocess.run(cmd_extract)

                # Generate concat list
                concat_list = os.path.join(tempfile.gettempdir(), "concat_list.txt")
                with open(concat_list, "w") as f:
                    for _ in range(10):
                        f.write(f"file '{tmp_clip}'\n")

                cmd_concat = [
                    "ffmpeg", "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_list,
                    "-c", "copy",
                    output_path
                ]
                subprocess.run(cmd_concat)
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(start_sec),
                    "-t", str(duration_sec),
                    "-i", self.current_path,
                    "-c", "copy",
                    output_path
                ]
                subprocess.run(cmd)
        else:
            # AUDIO ONLY (wav)
            if repeat:
                from pydub import AudioSegment
                full_audio = AudioSegment.from_file(self.current_path)
                loop = full_audio[self.loop_start:self.loop_end]
                if len(loop) == 0:
                    self.console.config(text="❌ Boucle vide, export annulé")
                    return
                loop_x10 = loop * 10
                loop_x10.export(output_path, format="wav")
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(start_sec),
                    "-t", str(duration_sec),
                    "-i", self.current_path,
                    "-vn",
                    "-acodec", "pcm_s16le",
                    "-ar", "48000",
                    "-ac", "2",
                    output_path
                ]
                subprocess.run(cmd)

        if destination == 'disk':
            self.console.config(text=f"✅ Exporté : {os.path.basename(output_path)}")
        else:
            # GDrive destination
            try:
                Brint(f"[GDRIVE] Uploading {output_path} as {media_base_name}")
                # The base name for Google Drive folder should be from the original media, not the temp export.
                # Assuming media_base_name is correctly derived from self.current_path earlier.
                upload_loop_to_drive(output_path, media_base_name) # Use media_base_name for folder, filename for file
                self.console.config(text=f"✅ Boucle {filename} envoyée sur Google Drive")
            finally:
                if os.path.exists(output_path):
                    os.remove(output_path)
                    Brint(f"[TEMP CLEANUP] Removed temporary GDrive export: {output_path}")

   
    #wavx10 

    def export_loop_wav_x10(self):
        if not self.loop_start or not self.loop_end:
            self.console.config(text="⚠️ Marqueurs A et B non définis")
            return

        input_path = self.current_path
        if not os.path.exists(input_path):
            self.console.config(text="❌ Fichier source introuvable")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("Fichiers WAV", "*.wav")],
            title="Sauvegarder la boucle A-B x10"
        )
        if not output_path:
            return

        # Charger audio entier
        full_audio = AudioSegment.from_file(input_path)
        loop = full_audio[self.loop_start:self.loop_end]

        if len(loop) == 0:
            self.console.config(text="❌ Boucle vide, export annulé")
            return

        # Répéter x10
        loop_x10 = loop * 10

        # Export
        loop_x10.export(output_path, format="wav")
        self.console.config(text=f"✅ Exporté en .wav x10 : {os.path.basename(output_path)}")


    # === METHODES TEMPO À AJOUTER DANS VideoPlayer ===
    def update_all_detected_notes_from_master(self):
        """Reconstruit les notes affichées à partir de la grille et des notes master"""
        source = getattr(self, "current_loop_master_notes", None)
        if not source or not self.grid_times:
            pass#Brint("[RHYTHM] ⚠️ Aucune current_loop_master_notes ou grille vide")
            self.all_detected_notes = []
            return

        self.all_detected_notes = []

        Brint("[DEBUG] 🔍 master_note_list (extrait) :")
        for note in source[:20]:
            start, end, pitch, conf = note
            Brint(f"[TBD] - {self.hms(start * 1000)} → {self.hms(end * 1000)} | Pitch: {pitch} | Confidence: {conf:.2f}")

        for i in range(len(self.grid_times)):
            t0 = self.grid_times[i]
            t1 = self.grid_times[i + 1] if i + 1 < len(self.grid_times) else t0 + 60.0 / self.tempo_bpm
            group = [
                (pitch, conf)
                for start, end, pitch, conf in source
                if not (end < t0 or start >= t1)
            ]
            self.all_detected_notes.append(group)
            Brint(f"[DEBUG] Subdiv {i:02d} ({self.hms(t0 * 1000)} → {self.hms(t1 * 1000)}) → {len(group)} note(s)")

        pass#Brint(f"[RHYTHM] 🎯 Notes recalculées pour {len(self.grid_times)} subdivisions")


    def cycle_subdivision_mode_backward(self):
        Brint(f"[DEBUG CYCLE] Avant changement → {len(self.current_loop.chords)} accords")

        modes = ALL_SUBDIVISION_MODES
        i = modes.index(self.subdivision_mode)
        self.subdivision_mode = modes[(i - 1) % len(modes)]
        pass#Brint(f"[RHYTHM] ⬅️ Mode subdivision : {self.subdivision_mode}")
        self.console.config(text=f"⬅️ Subdivision mode: {self.subdivision_mode}")
        
        self.build_rhythm_grid()
        self.compute_rhythm_grid_infos() # Ensure precomputed_grid_infos is fresh for the new mode
        self.update_all_detected_notes_from_master()  # ← très important
        Brint(f"[DEBUG CYCLE] Après update notes → accords = {len(self.current_loop.chords)}")

        # Remap persistent validated hits to the new grid
        self.remap_persistent_validated_hits()

        # 🔍 Debug : affichage des 10 premières notes de la master list
        Brint("[DEBUG] 🔍 master_note_list (extrait) :")
        for note in self.current_loop_master_notes[:10]:
            start, end, pitch, conf = note
            Brint(f"[TBD]  - {self.hms(start * 1000)} | Pitch: {pitch} | Confidence: {conf:.2f}")
        
        self.refresh_note_display()
        self.draw_rhythm_grid_canvas()
        self.draw_harmony_grid_overlay()
        if hasattr(self, "chord_editor_popup") and self.chord_editor_popup.winfo_exists():
            self.refresh_chord_editor()

        


    def current_rhythm_type(self):
        return "ternary" if "ternary" in self.subdivision_mode else "binary"


    def cycle_subdivision_mode(self):
        modes = ALL_SUBDIVISION_MODES
        i = modes.index(self.subdivision_mode)
        self.subdivision_mode = modes[(i + 1) % len(modes)]
        pass#Brint(f"[RHYTHM] ➡️ Mode subdivision : {self.subdivision_mode}")
        self.console.config(text=f"➡️ Subdivision mode: {self.subdivision_mode}")
        self.build_rhythm_grid()
        self.rebuild_loop_context()  # ← met à jour self.grid_subdivs ET chords si tu les relies dedans

        # Remap persistent validated hits to the new grid
        self.remap_persistent_validated_hits()

        self.update_all_detected_notes_from_master()  # ← très important

        # 🔍 Debug : affichage des 10 premières notes de la master list
        # Brint("[DEBUG] 🔍 master_note_list (extrait) :")
        # for note in self.current_loop_master_notes[:10]:
            # start, end, pitch, conf = note
            # Brint(f"[TBD]  - {self.hms(start * 1000)} | Pitch: {pitch} | Confidence: {conf:.2f}")
        
        
        
        self.refresh_note_display()
        self.draw_rhythm_grid_canvas()

    # === SYLLABLE SET MANAGEMENT ===
    def _get_syllable_key(self):
        return MODE_TO_SYLLABLE_KEY.get(self.subdivision_mode)

    def get_current_syllable_sequence(self):
        key = self._get_syllable_key()
        sets = RHYTHM_SYLLABLE_SETS.get(key, [])
        if not sets:
            return []
        idx = self.syllable_set_idx.get(key, 0) % len(sets)
        return sets[idx]["labels"]

    def get_current_syllable_description(self):
        key = self._get_syllable_key()
        sets = RHYTHM_SYLLABLE_SETS.get(key, [])
        if not sets:
            return ""
        idx = self.syllable_set_idx.get(key, 0) % len(sets)
        return sets[idx]["name"]

    def cycle_syllable_set(self):
        key = self._get_syllable_key()
        sets = RHYTHM_SYLLABLE_SETS.get(key, [])
        if not sets:
            self.console.config(text="⛔ No syllable sets for this mode")
            return
        idx = (self.syllable_set_idx.get(key, 0) + 1) % len(sets)
        self.syllable_set_idx[key] = idx
        self.build_rhythm_grid()
        self.draw_rhythm_grid_canvas()
        desc = sets[idx]["name"]
        self.console.config(text=f"🎵 Syllable set: {desc}")

    def cycle_syllable_set_backward(self):
        key = self._get_syllable_key()
        sets = RHYTHM_SYLLABLE_SETS.get(key, [])
        if not sets:
            self.console.config(text="⛔ No syllable sets for this mode")
            return
        idx = (self.syllable_set_idx.get(key, 0) - 1) % len(sets)
        self.syllable_set_idx[key] = idx
        self.build_rhythm_grid()
        self.draw_rhythm_grid_canvas()
        desc = sets[idx]["name"]
        self.console.config(text=f"🎵 Syllable set: {desc}")


    def get_rhythm_levels(self):
        """
        Retourne les durées (en ms) des niveaux de saut selon le tempo et le type de subdivision.
        """
        bpm = self.tempo_bpm
        if bpm <= 0:
            bpm = 60

        base_beat = 60000 / bpm
        rhythm_type = "ternary" if "ternary" in self.subdivision_mode else "binary"

        levels = {
            "bar": base_beat * 4,
            "beat": base_beat,
            "8th": base_beat / (3 if rhythm_type == "ternary" else 2),
            "16th": base_beat / (6 if rhythm_type == "ternary" else 4),
            "64th": base_beat / (48 if rhythm_type == "ternary" else 32)

        }
        Brint(f"[SCORE jumps] RHYTHMe jump → BPM={bpm:.2f} | bar={levels['bar']} | beat={levels['beat']}")


        return levels

    def get_subdivisions_per_beat(self, mode=None):
        """Return the number of grid subdivisions representing one beat.

        If *mode* is omitted, ``self.subdivision_mode`` is used. Unknown modes
        default to the binary eighth note resolution (2 subdivisions per beat).
        The helper understands both the internal subdivision modes (``binary8``,
        ``binary16``, ``ternary8``, ``ternary16``) and the extended keys used in
        :data:`RHYTHM_SYLLABLE_SETS` (``binary4``, ``ternary12`` …)."""

        if mode is None:
            mode = self.subdivision_mode

        mapping = {
            "binary4": 1,
            "binary8": 2,
            "binary16": 4,
            "ternary8": 3,
            "ternary16": 6,
            "ternary12": 3,
            "ternary24": 6,
            "ternary36": 9,
            "ternary32": 9,
        }

        return mapping.get(mode, 2)


    def snap_time_to_grid(self, time_ms, level):
        """
        Ramène time_ms au point RHYTHMique le plus proche selon le niveau.
        """
        delta = self.get_jump_duration_ms(level)
        snapped = round(time_ms / delta) * delta
        return int(snapped)
        
    def jump_playhead(self, direction, level):
        assert direction in (-1, 1), "Direction must be +1 or -1"

        original_level = level
        override_reason = ""

        if not self.is_loop_effectively_defined():
            # 🔁 Aucun loop actif → override durées en SECONDES
            override_seconds = {
                "beat": 10,
                "8th": 60,
                "16th": 300,
                "64th": 600
            }
            seconds = override_seconds.get(level, None)
            if seconds is not None:
                delta_ms = int(seconds * 500)
                override_reason = f"[NO LOOP] override {original_level} → {seconds:.3f}s"
                Brint(f"[JUMP] Aucun loop actif → {original_level} remplacé par {seconds:.3f}s ({delta_ms} ms)")
            else:
                delta_ms = self.get_jump_duration_ms(level)
        else:
            delta_ms = self.get_jump_duration_ms(level)
       

        mode = self.edit_mode.get() if hasattr(self, "edit_mode") else None

        if mode == "loop_start" and self.loop_start is not None:
            current_ms = self.loop_start
            Brint("[JUMP] Mode édition : loop_start")
        elif mode == "loop_end" and self.loop_end is not None:
            current_ms = self.loop_end
            Brint("[JUMP] Mode édition : loop_end")
        else:
            current_ms = int(self.playhead_time * 1000)
            Brint(f"[JUMP] Mode normal depuis {current_ms} ms")

        target_ms = current_ms + direction * delta_ms
        target_ms = self.snap_time_to_grid(target_ms, level)
        target_ms = max(0, target_ms)

        if mode == "loop_start":
            self.record_loop_marker("loop_start", milliseconds=target_ms, auto_exit=False)
        elif mode == "loop_end":
            self.record_loop_marker("loop_end", milliseconds=target_ms, auto_exit=False)
        else:
            self.safe_jump_to_time(target_ms, source="jump_playhead")
            self.safe_update_playhead(target_ms, source="jump_playhead")

        Brint(f"[TBD] ➡️ Jump {original_level} {direction:+} → {target_ms} ms (delta : {delta_ms} ms) {override_reason}")



    def get_jump_duration_ms(self, level):
        return self.get_rhythm_levels().get(level, 500)



    def jump_to_A(self):
        if not self.loop_start:
            self.console.config(text="⚠️ Aucun marqueur A défini")
            return
        ms = self.loop_start
        # self.jump_to_time(ms)
        self.safe_jump_to_time(ms, source="jump_to_A")
        # self.update_playhead_by_time(ms)
        self.safe_update_playhead(ms, source="jump_to_A")
        self.playhead_time = ms / 1000
        Brint(f"[TBD] 🎯 Jump to A : {ms} ms")

    def update_loop_menu(self):
        self.loop_menu.delete(0, tk.END)

        self.loop_menu.add_command(label="🎥 Reframe", command=self.reframe_current_media)
        self.loop_menu.add_command(label="🔍 Analyse", command=self.analyser_boucle)
        self.loop_menu.add_separator()
        self.loop_menu.add_command(label="💾 Sauvegarder A–B", command=lambda: self.root.after(10, self.build_export_menu, self.root)
)
        self.loop_menu.add_command(label="💾 Enregistrer boucle", command=self.save_current_loop)
        self.loop_menu.add_command(label="🗑️ Supprimer boucle", command=self.delete_selected_loop)
        self.loop_menu.add_separator()

        if hasattr(self, "saved_loops") and self.saved_loops:
            for i, loop in enumerate(self.saved_loops):
                label = f"🔁 {loop['name']}"
                self.loop_menu.add_command(label=label, command=lambda i=i: self.load_saved_loop(i))
        else:
            self.loop_menu.add_command(label="(aucune boucle)", state="disabled")

        Brint("[DEBUG] → open_chord_editor_all() called")






    def open_chord_editor_all(self):
        Brint("[DEBUG] → open_chord_editor_all() called")

        if not hasattr(self, "current_loop") or not isinstance(self.current_loop, LoopData):
            Brint("[ERROR] Aucun LoopData actif (current_loop est vide ou invalide)")
            self.console.config(text="⛔ Aucune boucle sélectionnée")
            return

        if not hasattr(self.current_loop, "mode") or not self.current_loop.mode:
            self.current_loop.mode = "ionian"

        if not hasattr(self, "grid_times") or not self.grid_times:
            if hasattr(self, "grid_subdivs"):
                self.grid_times = [t for _, t in self.grid_subdivs]
                Brint("[REMAP] 🔄 grid_times reconstruit depuis grid_subdivs")
            else:
                Brint("[ERROR open_chord_editor_all] Aucune grille disponible pour associer les notes.")
                return {}
                Brint(f"[DEBUG] → {len(self.grid_subdivs)} subdivisions détectées")
        self.compute_rhythm_grid_infos()  # ou équivalent si c'est ça qui remplit self.grid_times


        loop_duration_s = (self.current_loop.loop_end - self.current_loop.loop_start) / 1000
        self.subdivs_per_beat = round(len(self.grid_subdivs) / (loop_duration_s * self.current_loop.tempo_bpm / 60))
        Brint(f"[INFO] Estimation subdivs_per_beat = {self.subdivs_per_beat}")
        Brint(f"[DEBUG open_chord_editor_all] grid_subdivs = {getattr(self, 'grid_subdivs', '❌ absente')}")
        Brint(f"[DEBUG open_chord_editor_all] grid_times = {getattr(self, 'grid_times', '❌ absente')}")
        self.current_loop.map_notes_to_subdivs()
        subdiv_mapping = getattr(self.current_loop, "mapped_notes", {})
        if not subdiv_mapping:
            Brint("[WARN] Aucun mapping de note détecté après map_notes_to_subdivs()")
        Brint(f"[DEBUG] → {len(subdiv_mapping)} subdivisions avec notes mappées")

        popup = tk.Toplevel(self.root)
        self.chord_editor_popup = popup
        popup.title(f"Modifier accords/notes de '{self.current_loop.name}' (key={self.current_loop.key})")

        def on_popup_close():
            self.chord_editor_popup = None
            self.chord_editor_note_entries = []
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_popup_close)

        beats_per_measure = 4
        subdivs_per_beat = self.subdivs_per_beat
        total_subdivs = len(self.grid_subdivs)
        subdivs_per_measure = beats_per_measure * subdivs_per_beat
        if subdivs_per_measure == 0:
            Brint("[ERROR] subdivs_per_measure est 0 — impossible de diviser.")
            return
        total_measures = (total_subdivs + subdivs_per_measure - 1) // subdivs_per_measure



        # 🔢 Ajustement dynamique de la largeur du popup selon le nombre de mesures
        width_per_measure = 160  # ↔️ tu peux ajuster ici selon la densité visuelle voulue
        padding = 80  # marge fixe (scrollbar + bords)
        popup_width = total_measures * width_per_measure + padding
        popup.geometry(f"{popup_width}x700")
        Brint(f"[POPUP WIDTH] 📐 {total_measures} mesures × {width_per_measure}px + {padding}px = {popup_width}px")




        # popup.geometry("800x700")  # hauteur plus généreuse
        popup.attributes("-topmost", True)
        # 🎼 Champ éditable pour la clé de la boucle
        # key_frame = tk.Frame(popup)
        # key_frame.pack(pady=5)
        # tk.Label(key_frame, text="🎼 Tonalité (key):", font=("Arial", 9)).pack(side="left")
        mode_var = tk.StringVar(value=self.current_loop.mode or "ionian")
        key_var = tk.StringVar(value=self.current_loop.key or "C")
        # tk.Entry(key_frame, textvariable=key_var, width=10).pack(side="left")
        # Scrollable canvas
        container = tk.Frame(popup)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig("frame", width=e.width))

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")

        # Scroll region auto-ajustée
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # Support molette souris
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

        # Pour le reste du code (ajouts dynamiques)
        frame = scrollable_frame  # <== ton code utilise `frame` ensuite

        entry_vars = []
        degree_vars = []
        note_entry_vars = []  # À mettre en haut, avec entry_vars et degree_vars
        chord_entry_vars = []   # (measure_index, chord_var)
        degree_entry_vars = []  # (measure_index, degree_var)



        # Séquence de syllabes selon le mode
        label_seq = self.get_current_syllable_sequence()
        if not label_seq:
            label_seq = [str(i + 1) for i in range(subdivs_per_beat * beats_per_measure)]
            
        mode_key_frame = tk.Frame(frame)  # ⚠️ pas popup, sinon conflit avec scrollable
        mode_key_frame.pack(pady=5, fill="x")

        key_frame = tk.Frame(mode_key_frame)
        key_frame.pack(side="left", padx=10)
        tk.Label(key_frame, text="Key :").pack(side="left")
        key_entry = tk.Entry(key_frame, textvariable=key_var, width=4)
        key_entry.pack(side="left")

        mode_frame = tk.Frame(mode_key_frame)
        mode_frame.pack(side="left", padx=10)
        tk.Label(mode_frame, text="Mode :").pack(side="left")
        mode_selector = tk.OptionMenu(mode_frame, mode_var, *AVAILABLE_MODES)
        mode_selector.pack(side="left")

        def guess_chord_quality(chord_name):
            chord_name = chord_name.lower()
            if chord_name.endswith("°"):
                return "diminished"
            if "m" in chord_name and not "maj" in chord_name:
                return "minor"
            return "major"

        def on_chord_change(event, bp, chord_var, degree_var):
            chord = chord_var.get().strip()
            quality = guess_chord_quality(chord)
            deg = self.current_loop.degree_from_chord(chord)

            try:
                # Numérique ?
                deg_num = int(deg) if deg and deg.isdigit() else None
                if deg_num and 1 <= deg_num <= 7:
                    roman = MODES.get(self.current_loop.mode, MODES["ionian"])[deg_num - 1]
                else:
                    roman = deg.upper()
                
                # Appliquer la qualité au label
                if quality == "minor":
                    roman = roman.lower()
                elif quality == "diminished":
                    roman = roman.lower() + "°"
                # sinon (major), on garde le roman majuscule
                degree_var.set(roman)
            except:
                degree_var.set(deg or "?")

            Brint(f"[EDITOR EDIT] 🎵 Changement accord @beat {bp} → {chord} ➔ {degree_var.get()}")
            if event:
                event.widget.tk_focusNext().focus()
        def on_degree_change(event, bp, degree_var, chord_var):
            deg = degree_var.get().strip()
            if deg.isdigit():
                roman = MODES[self.current_loop.mode][int(deg) - 1]
                chord = self.current_loop.chord_from_degree(roman)
                Brint(f"[EDIT] Mode assisté : {deg} ➔ {roman} ➔ {chord}")
            else:
                chord = self.current_loop.chord_from_degree(deg)
                Brint(f"[EDIT] Mode brut : {deg} ➔ {chord}")
            chord_var.set(chord)

        def update_key_only(*args):
            new_key = key_var.get().strip().upper()
            previous_key = self.current_loop.key or "C"
            if not new_key or new_key == previous_key:
                return
            Brint(f"[KEY] ➡ {previous_key} → {new_key}")
            self.current_loop.key = new_key
            # self.current_loop.map_notes_to_subdivs()
            # for (_, chord_var), (_, degree_var) in zip(chord_entry_vars, degree_entry_vars):
                # deg = degree_var.get().strip()
                # if deg:
                    # new_chord = self.current_loop.chord_from_degree(deg)
                    # chord_var.set(new_chord)
                    # Brint(f"[KEY UPDATE] 🎵 {deg} → {new_chord}")
            for (_, chord_var), (_, degree_var) in zip(chord_entry_vars, degree_entry_vars):
                deg = degree_var.get().strip()
                if deg:
                    try:
                        # Recalculer et mettre à jour l'accord
                        new_chord = self.current_loop.chord_from_degree(deg)
                        chord_var.set(new_chord)
                        Brint(f"[KEY UPDATE] 🎵 {deg} → {new_chord}")

                        # ⚠️ Mettre à jour le champ degré aussi (dans le cas où un fallback ou mapping interne change)
                        # En appelant directement la fonction comme si un event venait de se produire
                        on_degree_change(None, 0, degree_var, chord_var)

                    except Exception as e:
                        chord_var.set("?")
                        Brint(f"[KEY UPDATE ERROR] {deg} → ❌ ({e})")



        def update_mode_only(*args):
            new_mode = mode_var.get()
            if new_mode == self.current_loop.mode:
                return
            Brint(f"[MODE] ➡ {self.current_loop.mode} → {new_mode}")
            self.current_loop.mode = new_mode
            self.current_loop.map_notes_to_subdivs()
        key_var.trace("w", update_key_only)
        mode_var.trace("w", update_mode_only)
        def apply_all_and_close():
            Brint("[SAVE] 🔄 Application manuelle des champs de note")

            # ➕ Mise à jour de la clé depuis le champ user
            new_key = key_var.get().strip().upper()
            self.current_loop.key = new_key
            Brint(f"[SAVE] 🎼 Key mise à jour : {new_key}")

            new_chords = []
            for (measure_index, chord_var), (_, degree_var) in zip(chord_entry_vars, degree_entry_vars):
                chord_raw = chord_var.get().strip()
                chord = normalize_chord_name(chord_raw)
                Brint(f"[SAVE] Accord brut '{chord_raw}' → normalisé '{chord}'")

                # chord = chord_var.get().strip().upper()
                if chord:
                    new_chords.append({
                        "beat_position": measure_index * beats_per_measure,
                        "chord": chord,
                        "root": chord,
                        "beat_end": (measure_index + 1) * beats_per_measure
                    })
            self.current_loop.chords = new_chords
            Brint(f"[SAVE] ✅ {len(new_chords)} accords sauvegardés")

            # Purge complète avant réapplication
            self.current_loop.master_note_list = []
            self.current_loop.map_notes_to_subdivs()
            if hasattr(self, "draw_harmony_grid_overlay"):
                Brint("[UI] 🔁 Redessin harmonique post-reset notes")
                self.draw_harmony_grid_overlay()

            for subdiv_i, var, t_ms, _ in note_entry_vars:
                make_handler(subdiv_i, var, t_ms)(None)

            if hasattr(self, "save_current_loop"):
                self.current_loop.key = key_var.get().strip().upper()
                self.current_loop.mode = mode_var.get().strip().lower()
                
                Brint("[TBD] === DEBUG SAUVEGARDE ===")
                Brint(f"[TBD] Key: {self.current_loop.key}")
                Brint(f"[TBD] Mode: {self.current_loop.mode}")
                Brint(f"[TBD] Chords: {self.current_loop.chords}")
                Brint(f"[TBD] Master Note List: {self.current_loop.master_note_list}")

                # ❌ Avant : self.save_current_loop()
                # ✅ Remplace par :
                self.force_save_current_loop()
                # self.save_current_loop()



                Brint("[SAVE] ✅ Boucle courante sauvegardée")
            else:
                Brint("[SAVE] ❌ Fonction save_current_loop non disponible")

            on_popup_close()

        # ---- Selection & toggle helpers ----
        self.selected_subdiv_index = None
        self.selected_subdiv_timestamp = None

        def focus_handler(subdiv_i, t_ms, widget):
            self.selected_subdiv_index = subdiv_i
            self.selected_subdiv_timestamp = t_ms
            self._selected_entry_widget = widget

        def toggle_selected_subdiv(event=None):
            if self.selected_subdiv_index is None:
                Brint("[TOGGLE] No subdiv selected")
                return
            self.toggle_subdiv_state_manual(self.selected_subdiv_index, self.selected_subdiv_timestamp)
            # update entry highlight
            for si, _, _, entry in note_entry_vars:
                if si == self.selected_subdiv_index:
                    if self.subdivision_state.get(si, 0) == 2:
                        entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)
                    else:
                        entry.configure(highlightthickness=0)
                    break


        for measure_index in range(total_measures):
            col = tk.Frame(frame)
            col.pack(side="left", padx=4)
            tk.Label(col, text=f"[MESURE {measure_index+1}]", font=("Arial", 10, "bold")).pack()

            # Chord unique de la mesure (position = beat 0)
            beat_pos = measure_index * beats_per_measure
            chord_data = self.current_loop.get_chord_at_beat(beat_pos)
            chord = chord_data.get("chord", "") if chord_data else ""
            degree = self.current_loop.degree_from_chord(chord) if chord else "?"

            tk.Label(col, text=f"[Accord: {chord}]", font=("Arial", 9)).pack()
            tk.Label(col, text=f"[Degré: {degree}]", font=("Arial", 9)).pack()
            
            chord_var = tk.StringVar(value=chord)
            degree_var = tk.StringVar(value=degree)
            chord_entry_vars.append((measure_index, chord_var))
            degree_entry_vars.append((measure_index, degree_var))

            chord_entry = tk.Entry(col, textvariable=chord_var, width=6)
            chord_entry.bind("<FocusOut>", lambda e, bp=beat_pos, cv=chord_var, dv=degree_var: on_chord_change(e, bp, cv, dv))
            chord_entry.pack()

            degree_entry = tk.Entry(col, textvariable=degree_var, width=6)
            degree_entry.bind("<FocusOut>", lambda e, bp=beat_pos, dv=degree_var, cv=chord_var: on_degree_change(e, bp, dv, cv))
            degree_entry.pack()
            chord_entry.bind("<Return>", lambda e, bp=beat_pos, cv=chord_var, dv=degree_var: on_chord_change(e, bp, cv, dv))
            degree_entry.bind("<Return>", lambda e, bp=beat_pos, dv=degree_var, cv=chord_var: on_degree_change(e, bp, dv, cv))
            # Vérifie s’il y a au moins un hit=2 dans la mesure
            has_hit_2 = any(
                getattr(self, "subdivision_state", {}).get(measure_index * subdivs_per_measure + k, 0) == 2
                for k in range(subdivs_per_measure)
            )



            for j in range(subdivs_per_measure):
                subdiv_index = measure_index * subdivs_per_measure + j
                if subdiv_index >= total_subdivs:
                    continue

                # Déterminer le numéro du beat (dans la mesure) et la syllabe
                beat_in_measure = j // subdivs_per_beat + 1
                syll_in_beat = j % subdivs_per_beat

                # Ajouter séparateur horizontal au début de chaque beat
                if syll_in_beat == 0:
                    sep_frame = tk.Frame(col)
                    sep_frame.pack(fill="x", pady=(6, 0))
                    tk.Label(sep_frame, text=f" Beat {beat_in_measure} ", anchor="w", font=("Arial", 9, "bold")).pack(side="left")
                    tk.Frame(sep_frame, height=1, width=100, bg="black").pack(side="left", fill="x", expand=True)

                _, t_subdiv_sec = self.grid_subdivs[subdiv_index]
                t_ms = t_subdiv_sec * 1000
                notes_list = subdiv_mapping.get(subdiv_index, [])

                # Use current syllable set
                syllabe = label_seq[j] if j < len(label_seq) else ""
                note_strs = [n["note"] if isinstance(n, dict) else str(n) for n in notes_list]
                Brint(f"[CHORD EDITOR] S{subdiv_index} | t={self.hms(t_ms)} | Beat={beat_in_measure} | Syllabe={syllabe} | Notes={','.join(note_strs)}")
                # Afficher la syllabe seule
                tk.Label(col, text=syllabe, font=("Arial", 9)).pack()

                note_var = tk.StringVar(value=",".join(note_strs))
                # note_var = tk.StringVar(value=",".join(notes_list))
                def make_handler(subdiv_i, note_var, t_ms):
                    def handler(event):
                        new_notes_raw = [n.strip() for n in note_var.get().split(",") if n.strip()]
                        old_notes = subdiv_mapping.get(subdiv_i, [])

                        if not new_notes_raw and not old_notes:
                            return  # ✅ rien à faire

                        Brint(f"[NOTES] 🔄 Modification @subdiv {subdiv_i}")

                        key = self.current_loop.key or "C"
                        mode = self.current_loop.mode or "ionian"

                        converted_notes = []
                        for note in new_notes_raw:
                            norm = normalize_note_entry(note, key, mode)
                            if norm:
                                converted_notes.append(norm)
                            else:
                                Brint(f"[SKIP] '{note}' rejetée")

                        if not converted_notes:
                            Brint(f"[WARN] ❌ Aucune note valide à ajouter pour subdiv {subdiv_i}")
                            return

                        # 🔄 Suppression des anciennes notes
                        before = len(self.current_loop.master_note_list)
                        self.current_loop.master_note_list = [
                            item for item in self.current_loop.master_note_list
                            if not (abs(item["timestamp_ms"] - t_ms) < 1 and item["note"] in old_notes)
                        ]
                        after = len(self.current_loop.master_note_list)
                        if before != after:
                            Brint(f"[EDIT] ➖ {before - after} notes supprimées à {t_ms:.1f}ms")

                        # ➕ Ajout des nouvelles notes propres
                        for note in converted_notes:
                            self.current_loop.master_note_list.append({
                                # "timestamp_ms": t_ms,
                                "timestamp_ms": int(t_ms),
                                "note": note
                            })
                            Brint(f"[EDIT] ➕ Note ajoutée : {note}@{t_ms:.0f}ms")

                        self.current_loop.map_notes_to_subdivs()
                        Brint(f"[EDIT] ✅ Subdiv {subdiv_i} mise à jour")
                        if hasattr(self, "draw_harmony_grid_overlay"):
                            Brint(f"[UI] 🔁 Redessin du canvas harmonique après modif subdiv {subdiv_i}")
                            self.draw_harmony_grid_overlay()


                    return handler










                note_entry = tk.Entry(col, textvariable=note_var, width=10)
                if has_hit_2 and getattr(self, "subdivision_state", {}).get(subdiv_index, 0) == 2:
                    note_entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)

                note_entry.bind("<FocusIn>", lambda e, si=subdiv_index, tm=t_ms: focus_handler(si, tm, e.widget))
                note_entry.bind("<FocusOut>", make_handler(subdiv_index, note_var, t_ms))
                note_entry.pack()
                note_entry_vars.append((subdiv_index, note_var, t_ms, note_entry))

                entry_vars.append((subdiv_index, note_var))
        # --- 🔧 PATCH COMPLÉTION AUTOMATIQUE PHANTOM UNIQUEMENT POUR LA DERNIÈRE MESURE ---
        total_rendered_subdivs = total_measures * subdivs_per_measure
        actual_last_col_subdivs = total_subdivs % subdivs_per_measure
        if actual_last_col_subdivs == 0:
            Brint("[PHANTOM] ✅ Dernière mesure complète, aucun ajout nécessaire")
        else:
            phantom_needed = subdivs_per_measure - actual_last_col_subdivs
            Brint(f"[PHANTOM] ➕ Ajout de {phantom_needed} subdivisions fantômes à la dernière colonne")
            last_col = frame.winfo_children()[-1]
            for i in range(phantom_needed):
                global_subdiv_index = total_subdivs + i
                j = actual_last_col_subdivs + i
                beat_in_measure = j // subdivs_per_beat + 1
                syll_in_beat = j % subdivs_per_beat

                # Si on est en début de beat, insérer séparateur
                if syll_in_beat == 0:
                    sep_frame = tk.Frame(last_col)
                    sep_frame.pack(fill="x", pady=(6, 0))
                    tk.Label(sep_frame, text=f" Beat {beat_in_measure} ", anchor="w", font=("Arial", 9, "bold"), fg="gray").pack(side="left")
                    tk.Frame(sep_frame, height=1, width=100, bg="gray").pack(side="left", fill="x", expand=True)
                    Brint(f"[PHANTOM] ➕ Séparateur Beat {beat_in_measure}")

                # Déterminer la bonne syllabe
                if self.subdivision_mode == "binary16":
                    syllables = [str(beat_in_measure), "y", "&", "a"]
                elif self.subdivision_mode == "ternary8":
                    syllables = [str(beat_in_measure), "T", "L"]
                elif self.subdivision_mode == "binary8":
                    syllables = [str(beat_in_measure), "n"]
                elif self.subdivision_mode == "ternary16":
                    syllables = [str(beat_in_measure), "t", "l", "n", "t", "l"]
                else:
                    syllables = [f".{k+1}" for k in range(subdivs_per_beat)]

                syllabe = syllables[syll_in_beat] if syll_in_beat < len(syllables) else "–"

                # Afficher la syllabe fantôme
                tk.Label(last_col, text=syllabe, font=("Arial", 9), fg="gray").pack()

                phantom_entry = tk.Entry(last_col, width=10)
                phantom_entry.insert(0, "")
                phantom_entry.configure(state="disabled", disabledforeground="gray", disabledbackground="#f0f0f0")
                phantom_entry.pack(pady=1)
                Brint(f"[PHANTOM] ➕ Subdiv fantôme {syllabe} (#{i+1})")

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        Brint("[SCROLL] 🔄 Scrollregion recalculée après ajout des lignes fantômes")

                    
        Brint(f"[DRAW PHANTOM] ✅ Fin génération éditeur de {total_measures} colonnes")
            
        # tk.Button(popup, text="✅ Appliquer", command=apply_all_and_close).pack(pady=10)
        # ➕ Zone boutons alignés
        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10, anchor="e", padx=20)

        tk.Button(btn_frame, text="✅ Appliquer", command=apply_all_and_close).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="Toggle Hit", command=toggle_selected_subdiv).pack(side="right", padx=(10, 0))
        popup.bind('<Control-r>', toggle_selected_subdiv)
        popup.bind('[', lambda e: self.offset_red_subdivisions(-1))
        popup.bind(']', lambda e: self.offset_red_subdivisions(+1))

        def reset_all_chords():
            Brint("[RESET] 🔁 Réinitialisation de tous les accords")
            for (_, chord_var), (_, degree_var) in zip(chord_entry_vars, degree_entry_vars):
                chord_var.set("")
                degree_var.set("")

        tk.Button(btn_frame, text="🗑️ Chords", command=reset_all_chords).pack(side="right", padx=(10, 0))

        def reset_all_notes():
            Brint("[RESET] 🔁 Réinitialisation de toutes les notes")
            for _, note_var, _, _ in note_entry_vars:
                note_var.set("")

        tk.Button(btn_frame, text="🗑️ Notes", command=reset_all_notes).pack(side="right", padx=(10, 0))

        self.chord_editor_note_entries = note_entry_vars






    def edit_current_chord_from_playhead(self, event=None):
        if not hasattr(self, "grid_times") or not self.grid_times:
            self.console.config(text="⛔ Grille RHYTHMique non disponible")
            return

        current_time = self.playhead_time  # en secondes
        closest_index = min(range(len(self.grid_times)),
                            key=lambda i: abs(self.grid_times[i] - current_time))

        bar_index = closest_index // 12  # 12 subdivisions par mesure (en ternaire 4/4)

        if 0 <= bar_index < len(self.chord_sequence):
            Brint(f"[TBD] 🎹 Édition accord pour mesure {bar_index + 1} (playhead)")
            self.open_chord_editor(bar_index)
        else:
            self.console.config(text=f"⚠️ Aucune mesure trouvée pour playhead {current_time:.2f}s")


    def edit_current_chord(self, event=None):
        try:
            index = self.result_box.index(tk.INSERT)
            line = int(index.split(".")[0])
            bar_index = line // 12  # 12 subdivisions par mesure (si ternaire 4/4)

            if 0 <= bar_index < len(self.chord_sequence):
                self.open_chord_editor(bar_index)
                Brint(f"[TBD] 🎹 Édition accord pour mesure {bar_index + 1}")
            else:
                self.console.config(text="⛔ Aucun accord associé à cette ligne")
        except Exception as e:
            Brint("[TBD] ❌ Erreur dans edit_current_chord :", e)


    def _handle_double_click_chord_edit(self, event, bar_index):
        self._double_click_detected = True
        self.open_chord_editor(bar_index)


    def open_chord_editor(self, bar_index):
        Brint("[EDITOR]chordeditor")
        if not (0 <= bar_index < len(self.chord_sequence)):
            self.console.config(text=f"❌ Mesure invalide : {bar_index}")
            return

        current_chord, current_root = self.chord_sequence[bar_index]

        popup = tk.Toplevel(self.root)

        popup.title(f"Modifier l'accord - Mesure {bar_index + 1}")
        
        # 🔢 Calcul largeur nécessaire pour l’éditeur
        # Tu peux adapter `width_per_measure` selon ton UI
        width_per_measure = 150
        padding = 100
        popup_width = total_measures * width_per_measure + padding
        popup.geometry(f"{popup_width}x700")
        Brint(f"[EDITOR POPUP WIDTH] 🧩 {total_measures} mesures × {width_per_measure}px + {padding}px = {popup_width}px")

        
        # popup.geometry("+300+300")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)  # facultatif, pour qu’elle passe devant


        tk.Label(popup, text=f"Mesure {bar_index + 1}").pack(pady=5)

        # chord_var = tk.StringVar(value=current_chord)
        root_var = tk.StringVar(value=current_root)

        frame = tk.Frame(popup)
        frame.pack(pady=5)
        # tk.Label(frame, text="Accord :").grid(row=0, column=0)
        # tk.Entry(frame, textvariable=chord_var, width=10).grid(row=0, column=1)
        tk.Label(frame, text="Fondamentale :").grid(row=1, column=0)
        tk.Entry(frame, textvariable=root_var, width=10).grid(row=1, column=1)

        def apply_changes():
            # new_chord = chord_var.get()
            new_root = root_var.get()
            Brint(f"[EDITOR DEBUG] ➕ set chord_sequence[{bar_index}] = ({new_root}, {new_root})")
            self.chord_sequence[bar_index] = (new_root, new_root)
            self.refresh_note_display()
            popup.destroy()

        tk.Button(popup, text="Valider", command=apply_changes).pack(pady=5)
        popup.bind("<Return>", lambda e: apply_changes())
        popup.grab_set()
        popup.focus_force()

    def build_rhythm_grid(self):
        """
        Reconstruit self.grid_times et self.grid_labels selon:
        - self.tempo_bpm
        - self.loop_start / loop_end (en ms)
        - self.subdivision_mode: one of ALL_SUBDIVISION_MODES
        """
        if not self.loop_start or not self.loop_end or not self.tempo_bpm:
            Brint("[BRG RHYTHM] ❌ Impossible de générer la grille : boucle ou tempo manquant")
            self.grid_times, self.grid_labels = [], []
            return

        loop_duration_sec = (self.loop_end - self.loop_start) / 1000.0
        bpm = self.tempo_bpm
        beats_per_bar = 4
        mode = self.subdivision_mode


        subdivs_per_beat = self.get_subdivisions_per_beat(mode)
        if subdivs_per_beat is None:
            Brint(f"[BRG RHYTHM] ❌ Mode subdivision inconnu : {mode}")
            return

        label_seq = self.get_current_syllable_sequence()
        if not label_seq:
            label_seq = []
            # Generic fallback: beat numbers on the first subdivision
            for beat in range(beats_per_bar):
                for s in range(subdivs_per_beat):
                    label_seq.append(str(beat + 1) if s == 0 else "")

        total_subdivs = int((bpm / 60) * loop_duration_sec * subdivs_per_beat)
        interval_sec = 60 / (bpm * subdivs_per_beat)

        self.grid_times = []
        self.grid_labels = []

        seq_len = len(label_seq)
        for i in range(total_subdivs):
            t = self.loop_start / 1000.0 + i * interval_sec
            self.grid_times.append(t)

            label = label_seq[i % seq_len] if seq_len else str((i % subdivs_per_beat) + 1)
            self.grid_labels.append(label)

            if i < 5:
                Brint(f"[BRG DEBUG] i={i} | t={self.hms(1000 * t)} hms")

        # 🔍 Filtrage pour rester dans la plage A–B (avec tolérance)
        loop_start_s = self.loop_start / 1000
        loop_end_s = self.loop_end / 1000
        subdiv_duration = 60 / (bpm * subdivs_per_beat)
        tolerance = subdiv_duration / 2

        zipped = list(zip(self.grid_labels, self.grid_times))
        filtered = [(lbl, t) for lbl, t in zipped if loop_start_s <= t <= loop_end_s + tolerance]

        before = len(zipped)
        after = len(filtered)
        if after < before:
            Brint(f"[BRG RHYTHM] ⚠️ {before - after} subdivisions hors A/B supprimées après build")

        # 💥 Correction : forcer le type list après zip(*)
        if filtered:
            labels, times = zip(*filtered)
            self.grid_labels, self.grid_times = list(labels), list(times)
        else:
            self.grid_labels, self.grid_times = [], []

        # ➕ Patch pour inclure la subdiv finale si elle manque encore
        if self.grid_times:
            last_time = self.grid_times[-1]
            if last_time + 0.5 * subdiv_duration < loop_end_s:
                next_t = last_time + subdiv_duration

                next_idx = len(self.grid_labels) % seq_len
                label = label_seq[next_idx] if seq_len else str((next_idx % subdivs_per_beat) + 1)

                if self.grid_labels and self.grid_labels[-1] == label:
                    Brint("[BRG PATCH] ⚠️ Duplicate syllable avoided at loop end")
                else:
                    self.grid_times.append(next_t)
                    self.grid_labels.append(label)
                    Brint(f"[BRG PATCH] ➕ Subdiv extra ajoutée : t={next_t:.3f}s > loop_end")

        self.grid_subdivs = list(enumerate(self.grid_times))

        Brint(f"[BRG RHYTHM] ✅ Grille générée : {len(self.grid_labels)} subdivisions ({mode})")
        Brint(f"[BRG BUILD RHYTHM GRID] subdivision_mode = {self.subdivision_mode}")



    def rebuild_grid_from_tempo(self, nb_measures=8, beats_per_measure=4, subdivision="ternary"):
        if not hasattr(self, "tempo_bpm"):
            self.console.config(text="⛔ Aucun tempo défini")
            return
        self.grid_times.clear()
        self.grid_labels.clear()
    

        beat_interval = 60.0 / self.tempo_bpm  # durée d'un temps en secondes
        beat1 = getattr(self, "beat1", self.loop_start / 1000.0)  # temps de départ en secondes

        # Subdivisions ternaires (1, T, L)
        if subdivision == "ternary":
            triplet_offsets = [0.0, beat_interval / 3, 2 * beat_interval / 3]
            steps_per_beat = 3
        else:
            # Subdivisions binaires (1, &, a)
            triplet_offsets = [0.0, beat_interval / 2]
            steps_per_beat = 2

        self.grid_times = []
        self.grid_labels = []

        for measure in range(1, nb_measures + 1):
            for beat in range(1, beats_per_measure + 1):
                for pos in range(1, steps_per_beat + 1):
                    t = beat1 + (measure - 1) * beats_per_measure * beat_interval \
                            + (beat - 1) * beat_interval \
                            + triplet_offsets[pos - 1]
                    self.grid_times.append(t)
                    self.grid_labels.append(f"{measure}.{beat}.{pos}")

    def _on_tempo_click(self, event):
        if str(self.tempo_entry['state']) == 'readonly':
            self._enable_tempo_edit()
            self.tempo_entry.focus_set()  # donne bien le focus pour taper



    def _enable_tempo_edit(self, event=None):
        self.tempo_entry.config(state="normal")
        self.console.config(text="📝 Modifie le tempo et appuie sur Entrée")
        # Démarre un timer pour désactiver après 10s si aucune action
        if hasattr(self, "_tempo_cooldown_id"):
            self.root.after_cancel(self._tempo_cooldown_id)
        self._tempo_cooldown_id = self.root.after(10000, self._disable_tempo_edit)

    def _disable_tempo_edit(self):
        self.tempo_entry.config(state="readonly")
        self.console.config(text="⏲️ Champ tempo désactivé (tape pour rééditer)")

    def _on_tempo_enter(self, event=None):
        try:
            value = float(self.tempo_var.get())
            self.set_tempo_bpm(value, source="entry")
        except ValueError:
            self.console.config(text="❌ Valeur tempo invalide")
        self._disable_tempo_edit()




    def dump_playhead_debug_log(self, n=10):
        Brint(f"\n[DEBUG LOG] Dernières {n} positions du playhead :")
        if not hasattr(self, "_debug_playhead_log"): self._debug_playhead_log = []

        for entry in self._debug_playhead_log[-n:]:
            t = int(entry["time"])
            x = entry["x"]
            mode = entry["mode"]
            status = ""
            if entry["awaiting"]:
                status += "⏳awaiting "
            if entry["frozen"]:
                status += "❄️frozen "
            Brint(f"[TBD]  - t={t}ms | x={x} | mode={mode} {status}")
            Brint(f"\n[STATS] x min = {self._debug_x_min}, x max = {self._debug_x_max}")




    def start_profiling_5s(self, event=None):
        import cProfile, pstats

        def run_for_5s():
            start = time.time()
            while time.time() - start < 5:
                # self.update_playhead_by_time(self.player.get_time())
                self.safe_update_playhead(self.player.get_time(), source="run_for_5s")
                time.sleep(0.015)

        # Brint("[TBD] 🟡 Profiling pendant 5 secondes...")
        # cProfile.runctx("run_for_5s()", globals(), locals(), filename="perf5s.stats")
        # Brint("[TBD] ✅ Profil terminé → perf5s.stats")
        # pstats.Stats("perf5s.stats").sort_stats("cumtime").print_stats(30)




    def profile_playhead_update(self, current_time_ms):
        def zone():
            # self.update_playhead_by_time(current_time_ms)
            self.safe_update_playhead(current_time_ms, source="profile_playhead_update")

        cProfile.runctx('zone()', globals(), locals(), 'zone.stats')
        p = pstats.Stats('zone.stats')
        p.strip_dirs().sort_stats('cumtime').print_stats(30)

    # --- Debug state window -------------------------------------------------
    def toggle_state_window(self, event=None):
        if self.state_window and self.state_window.winfo_exists():
            self.state_window.destroy()
            return

        self.state_window = tk.Toplevel(self.root)
        self.state_window.title("State Monitor")

        vars_to_show = [
            "playhead_time", "duration", "loop_start", "loop_end",
            "loop_zoom_ratio", "zoom_start", "zoom_end", "zoom_range",
            "loop_duration_s", "loop_pass_count",
        ]
        self._debug_labels = {}
        for name in vars_to_show:
            lbl = tk.Label(self.state_window, text="")
            lbl.pack(anchor="w")
            self._debug_labels[name] = lbl

        tk.Checkbutton(
            self.state_window,
            text="Pause each update",
            variable=self.pause_each_update,
        ).pack(anchor="w")
        # Step button removed (unused)

        tk.Label(self.state_window, text="Update delay (ms)").pack(anchor="w")
        tk.Entry(self.state_window, textvariable=self.update_delay_ms_var, width=6).pack(anchor="w")

        self.update_state_window()

    def update_state_window(self):
        if not (self.state_window and self.state_window.winfo_exists()):
            return
        zoom = self.get_zoom_context()
        values = {
            "playhead_time": f"{self.playhead_time:.3f}s" if getattr(self, "playhead_time", None) is not None else "N/A",
            "duration": self.duration,
            "loop_start": self.loop_start,
            "loop_end": self.loop_end,
            "loop_zoom_ratio": self.loop_zoom_ratio,
            "zoom_start": int(zoom.get("zoom_start", 0)),
            "zoom_end": int(zoom.get("zoom_end", 0)),
            "zoom_range": int(zoom.get("zoom_range", 0)),
            "loop_duration_s": getattr(self, "loop_duration_s", None),
            "loop_pass_count": getattr(self, "loop_pass_count", 0),
        }
        for name, lbl in self._debug_labels.items():
            try:
                if lbl.winfo_exists():
                    lbl.config(text=f"{name}: {values.get(name)}")
            except tk.TclError:
                continue
        self.state_window.after(100, self.update_state_window)

    def step_once(self):
        self.is_paused = False
        self.update_loop()



    def set_tempo_bpm(self, bpm, source="manual"):
        try:
            bpm = float(bpm)
            if bpm <= 0:
                raise ValueError
            self.tempo_bpm = bpm
            Brint(f"[TEMPO] 🎼 Nouveau tempo défini : {bpm:.2f} BPM (source={source})")

            if hasattr(self, "current_loop") and self.current_loop:
                self.current_loop.tempo_bpm = bpm
                Brint(f"[TEMPO][SYNC] tempo_bpm synchronisé dans current_loop : {bpm:.2f}")

            self.tempo_var.set(round(bpm, 2))
            ms_per_beat = round(60000 / bpm, 1)
            self.console.config(text=f"🎼 Tempo mis à jour ({source}) : {bpm:.2f} BPM → {ms_per_beat} ms / beat")
            self.tempo_label.config(text=f"{bpm:.2f} BPM • {ms_per_beat} ms/beat")

            # Recalculate one_bar_duration_ms and adjust B marker
            num_bars = getattr(self, 'mode_bar_bars', 1)
            if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
                self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * num_bars
            else:
                self.one_bar_duration_ms = 4000 * num_bars # Default
            Brint(f"[TEMPO CHANGE] Recalculated one_bar_duration_ms to {self.one_bar_duration_ms} ms for {num_bars} bar(s).")

            if hasattr(self, 'adjust_b_marker_if_mode_bar_enabled'):
                self.adjust_b_marker_if_mode_bar_enabled()

            if self.lock_tempo_var.get():
                Brint("[TEMPO] 🔒 Tempo verrouillé → mise à jour vitesse vidéo")
                self.update_video_speed_from_tempo()
        except:
            self.console.config(text="❌ BPM invalide")
            Brint("[TEMPO][ERROR] Valeur BPM invalide reçue")
            return

        Brint("[TEMPO] 🔄 Reconstruction complète de la grille rythmique")
        
        self.grid_times = []  # force reconstruction propre
        self.mapped_notes = {}

        self.build_rhythm_grid()
        self.draw_rhythm_grid_canvas()
        self.compute_rhythm_grid_infos()
        # Ensure LoopData instance keeps its grid in sync with the player
        if hasattr(self, "current_loop") and isinstance(self.current_loop, LoopData):
            self.grid_subdivs = [(i, t) for i, t in enumerate(self.grid_times)]
            self.current_loop.grid_times = self.grid_times
            self.current_loop.grid_subdivs = self.grid_subdivs

        # Remap persistent validated hits to the new grid
        self.remap_persistent_validated_hits()

        self.current_loop.map_notes_to_subdivs() # This should ideally happen after states are remapped if it depends on subdivision_state for any filtering
        self.refresh_note_display()


    def remap_persistent_validated_hits(self):
        """Map stored hit timestamps back to the current grid and set their states."""
        # Verify grid data exists first so we don't clear the state unnecessarily
        if not getattr(self, "precomputed_grid_infos", None):
            Brint("[REMAP_VALIDATED_HITS_ERROR] precomputed_grid_infos not available for remapping.")
            return

        if not getattr(self, "persistent_validated_hit_timestamps", None):
            Brint("[REMAP_VALIDATED_HITS] No persistent validated hit timestamps to remap.")
            return

        Brint("[REMAP_VALIDATED_HITS] Clearing old subdivision_state before remapping.")
        if not hasattr(self, "subdivision_state"):
            self.subdivision_state = {}
        self.subdivision_state.clear()

        Brint(f"[REMAP_VALIDATED_HITS] Remapping {len(self.persistent_validated_hit_timestamps)} persistent hit timestamps...")
        current_grid_times_map = {idx: info['t_subdiv_sec'] for idx, info in self.precomputed_grid_infos.items()}
        if not current_grid_times_map:
            Brint("[REMAP_VALIDATED_HITS_ERROR] current_grid_times_map is empty.")
            return

        grid_times_list = sorted(current_grid_times_map.values())
        intervals = [t2 - t1 for t1, t2 in zip(grid_times_list[:-1], grid_times_list[1:])]
        avg_interval_sec = sum(intervals) / len(intervals) if intervals else 0.5
        tolerance = avg_interval_sec / 2.0
        Brint(f"[HIT WINDOW] ℹ️ Tolerance set to {tolerance:.3f}s (1/2 of {avg_interval_sec:.3f}s)")

        for timestamp_sec in self.persistent_validated_hit_timestamps:
            new_closest_subdiv_idx = None
            min_delta = float('inf')
            for subdiv_idx, subdiv_t_sec in current_grid_times_map.items():
                delta = abs(subdiv_t_sec - timestamp_sec)
                if delta < min_delta:
                    min_delta = delta
                    new_closest_subdiv_idx = subdiv_idx

            if new_closest_subdiv_idx is not None and min_delta <= tolerance:
                self.subdivision_state[new_closest_subdiv_idx] = 2
                Brint(f"[REMAP_VALIDATED_HITS] Timestamp {timestamp_sec:.3f}s remapped to new subdiv {new_closest_subdiv_idx} (state 2) with delta {min_delta:.3f}s.")
            else:
                Brint(f"[REMAP_VALIDATED_HITS_WARN] Timestamp {timestamp_sec:.3f}s (min_delta {min_delta:.3f}s > tol {tolerance:.3f}s) could not be reliably remapped to any subdiv in the new grid.")

        


    def set_tempo_from_loop(self):
        try:
            loop_duration_sec = (self.loop_end - self.loop_start) / 1000.0
            if loop_duration_sec <= 0:
                raise ValueError
            nb_beats = 4  # par défaut, on suppose 1 mesure 4/4
            bpm = (60.0 * nb_beats) / loop_duration_sec
            self.set_tempo_bpm(bpm, source="A–B")
        except:
            self.console.config(text="❌ Impossible de calculer le tempo depuis la boucle")

    def modify_tempo(self, factor):
        self.set_tempo_bpm(self.tempo_bpm * factor, source=f"x{factor}")

    def update_video_speed_from_tempo(self):
        if not hasattr(self, 'player') or not self.lock_tempo_var.get():
            return
        try:
            ratio = self.tempo_bpm / self.tempo_ref
            self.player.set_rate(ratio)
            self.console.config(text=f"🎥 Vitesse lecture = x{ratio:.2f} (lock activé)")
        except:
            self.console.config(text="⚠️ Erreur set_rate")
    # TAP TEMPO amélioré
    def tap_tempo(self):
        import time
        now = time.perf_counter()
        self.tap_times.append(now)
        if len(self.tap_times) > 8:
            self.tap_times.pop(0)
        if len(self.tap_times) >= 2:
            intervals = [self.tap_times[i+1] - self.tap_times[i] for i in range(len(self.tap_times)-1)]
            avg_interval = sum(intervals) / len(intervals)
            if avg_interval > 0:
                tempo = 60.0 / avg_interval
                self.set_tempo_bpm(tempo, source="tap")

    
    

    def toggle_grid(self):
        self.grid_visible = not self.grid_visible
        if self.grid_visible:
            self.grid_canvas.pack(fill=X)
            self.grid_toggle_button.config(text='Grille ▼')
        else:
            self.grid_canvas.pack_forget()
            self.grid_toggle_button.config(text='Grille ▲')

    def update_rhythm_grid_visibility(self):
        self.rhythm_grid_enabled = self.show_rhythm_var.get()
        self.draw_rhythm_grid_canvas()

    def update_harmony_grid_visibility(self):
        self.harmony_grid_enabled = self.show_harmony_var.get()
        self.draw_harmony_grid_overlay()

    def toggle_mode_bar(self, event=None): # Add event=None if it's directly bound to a key
        self.mode_bar_enabled = not self.mode_bar_enabled
        num_bars = getattr(self, 'mode_bar_bars', 1)

        if self.mode_bar_enabled:
            if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
                self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * num_bars
            else:
                self.one_bar_duration_ms = 4000 * num_bars # Default
            Brint(f"[MODE BAR] Toggled ON. Duration for {num_bars} bar(s): {self.one_bar_duration_ms} ms")
            self.console.config(text=f"Mode Bar: B = A + {num_bars} bar(s)")
        else:
            # Mode bar is toggled OFF
            self.mode_bar_bars = 1 # Reset bar count
            num_bars = 1 # Ensure num_bars reflects the reset for the immediate recalculation
            if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
                self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * num_bars
            else:
                self.one_bar_duration_ms = 4000 * num_bars # Default
            Brint(f"[MODE BAR] Toggled OFF. Bars reset to 1. Duration for 1 bar: {self.one_bar_duration_ms} ms")
            self.console.config(text="Mode Bar: OFF (bars reset to 1)")

        # Call the method to adjust B marker
        if hasattr(self, 'adjust_b_marker_if_mode_bar_enabled'):
            self.adjust_b_marker_if_mode_bar_enabled()
        else:
            Brint("[MODE BAR] adjust_b_marker_if_mode_bar_enabled method not yet implemented.")

    def adjust_b_marker_if_mode_bar_enabled(self):
        if not self.mode_bar_enabled:
            Brint("[MODE BAR] Adjust B: Mode bar is OFF. No change to B.")
            return

        if self.loop_start is None:
            Brint("[MODE BAR] Adjust B: Loop start (A) is not defined. No change to B.")
            return

        if not hasattr(self, 'one_bar_duration_ms') or self.one_bar_duration_ms <= 0:
            Brint(f"[MODE BAR] Adjust B: Invalid one_bar_duration_ms ({getattr(self, 'one_bar_duration_ms', 'N/A')}). No change to B.")
            return

        video_duration = self.player.get_length()
        if not video_duration or video_duration <= 0:
            Brint("[MODE BAR] Adjust B: Video duration not available. No change to B.")
            return

        new_loop_end = self.loop_start + self.one_bar_duration_ms

        # Clamp new_loop_end to be within video duration and not before loop_start
        new_loop_end = max(self.loop_start + 1, new_loop_end) # Ensure B is at least 1ms after A
        new_loop_end = min(new_loop_end, video_duration)

        if new_loop_end != self.loop_end:
            self.loop_end = new_loop_end
            Brint(f"[MODE BAR] Adjusted B marker to {self.loop_end} ms (A + 1 bar at {self.one_bar_duration_ms}ms/bar)")

            # Update current_loop object as well
            if hasattr(self, 'current_loop') and self.current_loop:
                self.current_loop.loop_end = self.loop_end
                Brint(f"[MODE BAR] current_loop.loop_end also updated to {self.current_loop.loop_end}")

            # Explicitly update loop_duration_s for the main update_loop
            if self.loop_start is not None and self.loop_end is not None and self.loop_end > self.loop_start:
                self.loop_duration_s = (self.loop_end - self.loop_start) / 1000.0
                Brint(f"[MODE BAR] Updated self.loop_duration_s to {self.loop_duration_s:.3f}s")
            else:
                self.loop_duration_s = None
                Brint(f"[MODE BAR] Loop became invalid or undefined, self.loop_duration_s set to None")

            # Check if we need to jump the player to loop_start
            playhead_must_jump_to_A = False
            if self.playhead_time is not None:
                playhead_must_jump_to_A = (self.playhead_time * 1000) > self.loop_end

            if playhead_must_jump_to_A:
                self.last_loop_jump_time = time.perf_counter() # Standard reset for a jump to A
                Brint(f"[MODE BAR] Playhead past new B. Reset last_loop_jump_time for jump to A: {self.last_loop_jump_time:.3f}")
                # The existing call to safe_jump_to_time(self.loop_start, ...) for this case should remain later in the code if it exists,
                # or be added if it was removed. The subtask for previous step mentioned it was there.
            else:
                # Maintain current relative playhead position by adjusting last_loop_jump_time
                # This prevents visual jump to A if audio is not jumping to A.
                current_playback_rate = self.player.get_rate() or 1.0
                if current_playback_rate == 0:
                    current_playback_rate = 1.0  # Avoid division by zero

                if self.playhead_time is not None:
                    # playhead_time is in seconds, loop_start is in ms
                    current_offset_from_A_media_seconds = self.playhead_time - (self.loop_start / 1000.0)

                    # How much unscaled (real) time has passed for the playhead to reach its current position from A
                    current_offset_real_seconds = current_offset_from_A_media_seconds / current_playback_rate

                    self.last_loop_jump_time = time.perf_counter() - current_offset_real_seconds
                    Brint(
                        f"[MODE BAR] Adjusted last_loop_jump_time to maintain playhead position: {self.last_loop_jump_time:.3f} (current_offset_real_seconds: {current_offset_real_seconds:.3f})"
                    )
                else:
                    self.last_loop_jump_time = time.perf_counter()
                    Brint("[MODE BAR] Playhead time undefined; last_loop_jump_time reset.")

            self.needs_refresh = True
            self.refresh_static_timeline_elements()
            self.maybe_adjust_zoom_if_out_of_frame() # Or auto_zoom_on_loop_markers(force=True)
            self.invalidate_jump_estimators()

            # It might be necessary to update the playhead if it was past the new B
            if hasattr(self, 'playhead_time') and self.playhead_time and self.playhead_time * 1000 > self.loop_end:
                self.safe_jump_to_time(self.loop_start, source="Adjust B - Playhead Reset")
        else:
            Brint(f"[MODE BAR] Adjust B: B marker already correctly positioned at {self.loop_end} ms. No change.")

    def increase_mode_bar_bars(self, event=None):
        if not hasattr(self, 'mode_bar_enabled') or not self.mode_bar_enabled:
            Brint("[MODE BAR BARS] Increase: Mode bar is OFF. No change.")
            return

        if not hasattr(self, 'mode_bar_bars'):
            self.mode_bar_bars = 1

        self.mode_bar_bars += 1
        Brint(f"[MODE BAR BARS] Increased to {self.mode_bar_bars} bar(s).")

        # Recalculate one_bar_duration_ms (incorporating self.mode_bar_bars)
        if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
            self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * self.mode_bar_bars
        else:
            self.one_bar_duration_ms = 4000 * self.mode_bar_bars # Default
        Brint(f"[MODE BAR BARS] Recalculated one_bar_duration_ms to {self.one_bar_duration_ms}ms for {self.mode_bar_bars} bar(s).")

        if hasattr(self, 'adjust_b_marker_if_mode_bar_enabled'):
            self.adjust_b_marker_if_mode_bar_enabled()

        if hasattr(self, 'console'):
            self.console.config(text=f"Mode Bar: B = A + {self.mode_bar_bars} bar(s)")

    def decrease_mode_bar_bars(self, event=None):
        if not hasattr(self, 'mode_bar_enabled') or not self.mode_bar_enabled:
            Brint("[MODE BAR BARS] Decrease: Mode bar is OFF. No change.")
            return

        if not hasattr(self, 'mode_bar_bars'):
            self.mode_bar_bars = 1 # Should not happen if mode is ON, but defensive

        if self.mode_bar_bars > 1:
            self.mode_bar_bars -= 1
            Brint(f"[MODE BAR BARS] Decreased to {self.mode_bar_bars} bar(s).")

            # Recalculate one_bar_duration_ms
            if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
                self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * self.mode_bar_bars
            else:
                self.one_bar_duration_ms = 4000 * self.mode_bar_bars # Default
            Brint(f"[MODE BAR BARS] Recalculated one_bar_duration_ms to {self.one_bar_duration_ms}ms for {self.mode_bar_bars} bar(s).")

            if hasattr(self, 'adjust_b_marker_if_mode_bar_enabled'):
                self.adjust_b_marker_if_mode_bar_enabled()

            if hasattr(self, 'console'):
                self.console.config(text=f"Mode Bar: B = A + {self.mode_bar_bars} bar(s)")
        else:
            Brint(f"[MODE BAR BARS] Already at minimum 1 bar. No change.")
            if hasattr(self, 'console'):
                self.console.config(text=f"Mode Bar: B = A + {self.mode_bar_bars} bar(s) (min)")

    def get_or_create_video_folder(drive):
        return get_or_create_subfolder(ROOT_FOLDER_ID, "videopyplayer", drive)

    
    def open_save_menu(self):
        menu = Toplevel(self.root)
        menu.title("Sauvegarder la boucle")
        menu.geometry("+300+300")

        var_repeat = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(menu, text="Coller la boucle x10", variable=var_repeat)
        chk.pack(pady=5)

        Button(menu, text="💾 Save to HDD", command=lambda: (
            self.export_loop_wav_x10() if var_repeat.get() else self.save_ab_to_mp3(repeat=False),
            menu.destroy()
        ), width=20).pack(pady=5)
        Button(menu, text='Tap Tempo (T)', command=self.tap_tempo).pack(pady=5)
        Button(menu, text="☁️ Save to GDrive", command=lambda: (self.export_loop_and_upload_to_drive(repeat=var_repeat.get()), menu.destroy()), width=20).pack(pady=5)
        Button(menu, text="🟪 PY: Save .py to GDrive", command=lambda: (self.upload_current_py_to_drive(), menu.destroy()), width=25).pack(pady=5)

    
    def upload_current_py_to_drive(self):
        drive = authenticate()
        folder_id = get_or_create_subfolder(ROOT_FOLDER_ID, "videopyplayer", drive)

        # Repère le script .py actuel
        try:
            script_path = os.path.realpath(__file__)
        except NameError:
            Brint("[TBD] ❌ __file__ non défini. Ce script n'est pas exécuté comme un fichier standard.")
            return

        if not os.path.exists(script_path):
            Brint(f"[TBD] ❌ Fichier introuvable : {script_path}")
            return

        # Compte les fichiers playerX.py déjà présents
        existing = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false"
        }).GetList()

        numbers = [int(f['title'][6:-3]) for f in existing if f['title'].startswith('player') and f['title'].endswith('.py') and f['title'][6:-3].isdigit()]
        next_number = max(numbers, default=0) + 1
        target_name = f"player{next_number}.py"

        file_drive = drive.CreateFile({
            'title': target_name,
            'parents': [{'id': folder_id}]
        })
        file_drive.SetContentFile(script_path)
        file_drive.Upload()
        Brint(f"[TBD] ✅ Script {os.path.basename(script_path)} uploadé comme {target_name}")
        self.log_to_console(f"✅ Script {os.path.basename(script_path)} uploadé comme {target_name}")

    def open_given_file(self, path, spawn_new_instance=False):
        """Charge un fichier donné directement, sans repasser par le file dialog."""

        if not path:
            Brint("[OPEN] ❌ Chemin de fichier invalide")
            if hasattr(self, "console"):
                self.console.config(text="⛔ Invalid file path")
            return

        if spawn_new_instance:
            import subprocess
            import sys
            subprocess.Popen([sys.executable, os.path.abspath(__file__), path])
            self.root.destroy()
            sys.exit(0)
            return

        if not os.path.exists(path):
            Brint(f"[OPEN] ❌ Média introuvable : {path}")
            if hasattr(self, "console"):
                self.console.config(text=f"⛔ File not found: {path}")
            return

        self.current_path = path
        self.root.after(1000, self.load_screen_zoom_prefs)


        # --- faststart remux (si tu veux le garder)
        # self.faststart_remux(path)  # Décommente si besoin

        self.media = self.instance.media_new(path)
        self.load_saved_loops()
        self.player.set_media(self.media)
        self.player.set_hwnd(self.canvas.winfo_id())
        self.apply_crop()
        self.audio_power_data = None
        self.audio_power_max = 0.0
        import threading as _thread
        _thread.Thread(target=self._compute_audio_power_data, daemon=True).start()

        self.playhead_time = 0.0
        self.last_jump_target_ms = 0
        self.safe_update_playhead(0, source="open_given_file")

        self.player.play()
        self.root.after(1000, self.reset_force_playhead_time)

        if hasattr(self, "player"):
            self.player.audio_set_mute(False)

        self.safe_update_playhead(0, source="open_given_file2")
        self.root.after(100, self.update_loop)
        self.console.config(text=f"▶️ Playing: {os.path.basename(path)}")
        import threading
        threading.Thread(target=self._run_beat1_detection_from_scanfile, daemon=True).start()

        if dbflag:
            pass #Brint(f"[DEBUG] open_given_file(): tentative de get_length() = {self.player.get_length()} ms")

        self.add_recent_file(path)
    
    
    def _browse_and_open(self, win):
        win.destroy()
        self.open_file()  # appelle ton open_file() existant

    def _open_from_recent(self, path, win):
        Brint(f"[TBD] 🕘 Ouverture du fichier récent : {path}")
        win.destroy()
        self.open_given_file(path)
        self.needs_refresh = True
        self.refresh_static_timeline_elements()

    def show_open_menu(self):
        top = Toplevel(self.root)
        top.title("Ouvrir un fichier")
        Label(top, text="📁 Choisir un fichier").pack(pady=5)

        Button(top, text="🔍 Parcourir...", command=lambda: self._browse_and_open(top)).pack(fill="x", padx=10, pady=5)

        if hasattr(self, "recent_files") and self.recent_files:
            Label(top, text="🕘 Fichiers récents :").pack(pady=5)
            for path in self.recent_files:
                if os.path.exists(path):
                    Button(top, text=os.path.basename(path), command=partial(self._open_from_recent, path, top)).pack(fill="x", padx=10)

        # Section Save
        Label(top, text="💾 Options de sauvegarde :").pack(pady=5)

        Button(top, text="🟪 PY: Save .py to GDrive", command=lambda: (
            self.upload_current_py_to_drive(),
            top.destroy()
        ), width=25).pack(pady=5)    
    #recent files
        #recentfiles
    def load_recent_files(self):
        try:
            with open(RECENT_FILES_PATH, "r", encoding="utf-8") as f:
                self.recent_files = json.load(f)
        except Exception:
            self.recent_files = []

    def quick_open_recent(self):
        if not hasattr(self, 'recent_files') or not self.recent_files:
            self.console.config(text="⚠️ Aucun fichier récent")
            return

        top = Toplevel(self.root)
        top.title("Fichiers récents")
        Label(top, text="Choisissez un fichier :").pack(pady=5)

        for path in self.recent_files:
            Button(top, text=os.path.basename(path), command=lambda p=path: self.open_file(p)).pack(fill="x")
    
    
    def add_recent_file(self, path):
        """Ajoute un fichier média aux fichiers récents, enregistre la loop courante associée, et met à jour recent_files.json"""
        # 🔁 Chargement de la structure complète depuis le fichier JSON
        try:
            with open(RECENT_FILES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):  # support ancien format simple
                    data = {
                        "recent_paths": data,
                        "last_loops": {},
                        "auto_load_last_file": True,
                        "auto_load_last_loop": True
                    }
        except Exception as e:
            Brint(f"[RECENT] ⚠️ Fichier recent_files.json non trouvé ou corrompu : {e}")
            data = {
                "recent_paths": [],
                "last_loops": {},
                "auto_load_last_file": True,
                "auto_load_last_loop": True
            }

        paths = data.get("recent_paths", [])
        if path in paths:
            paths.remove(path)
        paths.insert(0, path)
        paths = paths[:3]
        data["recent_paths"] = paths

        # 🔁 Mise à jour de la dernière boucle associée à ce média
        loop_name = getattr(self.current_loop, "name", None)
        if loop_name:
            data.setdefault("last_loops", {})[path] = loop_name

        # 🔁 Valeurs par défaut (sécurité)
        data.setdefault("auto_load_last_file", True)
        data.setdefault("auto_load_last_loop", True)

        # 💾 Sauvegarde dans le fichier JSON
        try:
            with open(RECENT_FILES_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            Brint(f"[RECENT] ✅ Ajouté : {path} | Dernière loop = {loop_name}")
        except Exception as e:
            Brint(f"[TBD] ❌ Erreur lors de l'écriture dans recent_files.json : {e}")

        # 🧠 Mise à jour interne pour menu fichiers récents
        self.recent_files = paths
        
        
        
        
        
 #ZOOMVIDEO

    # --- Fonctions principales ---

    def abloops_json_path(self):
        base = os.path.splitext(os.path.basename(self.current_path))[0]
        return os.path.join(os.path.dirname(self.current_path), f".{base}.abloops.json")


    def load_saved_loops(self):
        Brint("[INFO] Loading saved loops...")
        self.saved_loops = []
        if not hasattr(self, "current_path") or not self.current_path:
            Brint("[WARNING] Aucun fichier ouvert, arrêt du chargement de boucles.")
            return

        try:
            path = self.abloops_json_path()
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                raw_loops = data if isinstance(data, list) else data.get("loops", [])

                # ✅ Validation juste après chargement brut


                valid_loops = []
                for loop in raw_loops:
                    is_valid, reason = self.validate_loop_data(loop)
                    if is_valid:
                        valid_loops.append(loop)
                    else:
                        Brint(f"[WARNING] Boucle '{loop.get('name', 'Unnamed')}' ignorée : {reason}")
                self.saved_loops = valid_loops


                Brint(f"[TBD] ✅ {len(self.saved_loops)} boucles valides chargées depuis {path}")
                for loop in self.saved_loops:
                    Brint(f"[LOOP LOAD] '{loop['name']}' tempo_bpm = {loop.get('tempo_bpm')}")

            else:
                Brint(f"[INFO] Aucun fichier de boucles trouvé à {path}")
        except Exception as e:
            Brint(f"[TBD] ❌ Erreur chargement boucles : {e}")

        # ⬇ Fallback name si aucune boucle sélectionnée
        base_name = self.sanitize_filename(os.path.splitext(os.path.basename(self.current_path))[0])
        if not hasattr(self, "selected_loop_name") or not self.selected_loop_name:
            default_name = f"{base_name}_loop1" if self.saved_loops else base_name
            self.set_selected_loop_name(default_name, source="load_saved_loops (fallback)")

        self.needs_refresh = True
        self.refresh_static_timeline_elements()
        # self.GlobXa, self.GlobXb = self.get_loop_zoom_range()
        if self.saved_loops:
            self.current_loop = LoopData.from_dict(self.saved_loops[0])
            Brint(f"[DEBUG] current_loop défini automatiquement : {self.current_loop.name} | A={self.current_loop.loop_start} | B={self.current_loop.loop_end}")
        else:
            self.current_loop = None
            Brint("[DEBUG] current_loop est None (aucune boucle chargée)")


    def save_loops_to_file(self):
        if not hasattr(self, "current_path") or not self.current_path:
            return
        try:
            path = self.abloops_json_path()
            if os.path.exists(path):
                backup_path = path + ".bak"
                try:
                    shutil.copy2(path, backup_path)
                    Brint(f"[UNDO] Backup enregistré dans {backup_path}")
                except Exception as e:
                    Brint(f"[UNDO] ❌ Échec de la sauvegarde de backup: {e}")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "loops": self.saved_loops
                }, f, indent=2)
            Brint(f"[TBD] 💾 Boucles sauvegardées dans {path}")
            Brint(f"[NHIT] Saved hits with loop to file: {path} | {self.abph_stamp()}")
        except Exception as e:
            Brint(f"[TBD] ❌ Erreur sauvegarde boucles: {e}")

    def restore_loops_from_backup(self, event=None):
        if not hasattr(self, "current_path") or not self.current_path:
            return
        path = self.abloops_json_path()
        backup_path = path + ".bak"
        if not os.path.exists(backup_path):
            self.log_to_console("❌ Aucun backup à restaurer")
            Brint(f"[UNDO] Aucun backup trouvé à {backup_path}")
            return
        try:
            shutil.copy2(backup_path, path)
            self.load_saved_loops()
            self.log_to_console("↩️ Boucles restaurées")
            Brint(f"[UNDO] Boucles restaurées depuis {backup_path}")
        except Exception as e:
            Brint(f"[UNDO] ❌ Erreur restauration backup: {e}")

    def save_temp_loop(self):
        """Save current loop to a temporary JSON file."""
        if not hasattr(self, "temp_loop_save_path") or not self.temp_loop_save_path:
            return
        if not hasattr(self, "current_loop") or not isinstance(self.current_loop, LoopData):
            return
        try:
            with open(self.temp_loop_save_path, "w", encoding="utf-8") as f:
                json.dump({"loops": [self.current_loop.to_dict()]}, f, indent=2)
            Brint(f"[TEMP SAVE] Loop written to {self.temp_loop_save_path}")
        except Exception as e:
            Brint(f"[TEMP SAVE ERROR] {e}")

    def cleanup_temp_loop(self):
        if getattr(self, "temp_loop_save_path", None) and os.path.exists(self.temp_loop_save_path):
            try:
                os.remove(self.temp_loop_save_path)
                Brint(f"[TEMP SAVE] Removed {self.temp_loop_save_path}")
            except Exception as e:
                Brint(f"[TEMP SAVE ERROR] Unable to remove temp file: {e}")

    def on_subdiv_validated(self, subdiv_index):
        """Called when a subdivision reaches red (state=3)."""
        Brint(f"[AUTO SAVE] Subdiv {subdiv_index} validated → temp save")
        self.save_temp_loop()

    def on_app_close(self):
        self.cleanup_temp_loop()
        self.root.destroy()




    def apply_crop(self):
        if hasattr(self, 'player') and self.player.get_media():
            video_w = self.player.video_get_width()
            video_h = self.player.video_get_height()
            if video_w <= 0 or video_h <= 0:
                video_w, video_h = 1920, 1080

            # ⚡ Ne plus changer crop_w et crop_h en fonction du zoom
            crop_w = video_w
            crop_h = video_h

            geom = f"{crop_w}x{crop_h}+{self.global_crop_x}+{self.global_crop_y}"
            self.player.video_set_crop_geometry(geom)

            # 📢 Seul le scale change !
            self.player.video_set_scale(self.global_zoom_level)

            Brint(f"[TBD] 🎯 Crop fixé: {geom} | Zoom visuel: {self.global_zoom_level:.2f}")
            self.update_pan(user_action="Zoom")
        # def zoom_in(self):
        # previous_zoom = self.global_zoom_level
        # self.global_zoom_level = min(self.global_zoom_level + self.zoom_step, 5.0)
        # self.apply_crop()
        # self.save_loops_to_file()
    def zoom_in(self):
        previous_zoom = self.global_zoom_level
        self.global_zoom_level = min(self.global_zoom_level + self.zoom_step, 5.0)

        video_w = self.player.video_get_width()
        video_h = self.player.video_get_height()
        if video_w <= 0 or video_h <= 0:
            video_w, video_h = 1920, 1080

        # Avant zoom : centre actuel
        old_crop_w = float(video_w / previous_zoom)
        old_crop_h = float(video_h / previous_zoom)
        center_x = self.global_crop_x + old_crop_w // 2
        center_y = self.global_crop_y + old_crop_h // 2

        # Après zoom : nouvelles dimensions
        new_crop_w = float(video_w / self.global_zoom_level)
        new_crop_h = float(video_h / self.global_zoom_level)

        # Recalibrer pour conserver le centre
        self.global_crop_x = center_x - new_crop_w // 2
        self.global_crop_y = center_y - new_crop_h // 2

        self.apply_crop()
        self.save_loops_to_file()
        # self.save_zoom_prefs()

    def zoom_out(self):
        previous_zoom = self.global_zoom_level
        self.global_zoom_level = max(self.global_zoom_level - self.zoom_step, 1.0)
        self.apply_crop()
        self.save_loops_to_file()
        # self.save_zoom_prefs()
        
    def pan_left(self):
        self.global_crop_x -= self.pan_step
        self.update_pan(user_action="Pan Left")
        self.save_loops_to_file()
        # self.save_zoom_prefs()
        
    def pan_right(self):
        self.global_crop_x += self.pan_step
        self.update_pan(user_action="Pan Right")
        self.save_loops_to_file()
        # self.save_zoom_prefs()



    def pan_up(self):
        self.global_crop_y += self.pan_step  # 🛠️ corrigé : déplacer vers le haut = augmenter Y dans VLC
        self.update_pan(user_action="Pan Up")
        self.save_loops_to_file()
        # self.save_zoom_prefs()

    def pan_down(self):
        self.global_crop_y -= self.pan_step  # 🛠️ corrigé : déplacer vers le bas = diminuer Y dans VLC
        self.update_pan(user_action="Pan Down")
        self.save_loops_to_file()
        # self.save_zoom_prefs()

    def update_pan(self, user_action="UNKNOWN"):
        Brint(f"🔵 [ACTION] Utilisateur a demandé : {user_action}")
        if hasattr(self, 'player') and self.player.get_media():
            video_w = self.player.video_get_width()
            video_h = self.player.video_get_height()
            if video_w <= 0 or video_h <= 0:
                video_w, video_h = 1920, 1080

            crop_w = video_w  # ⚡ FIXÉ
            crop_h = video_h  # ⚡ FIXÉ

            geom = f"{crop_w}x{crop_h}+{self.global_crop_x}+{self.global_crop_y}"
            self.player.video_set_crop_geometry(geom)

            # Debug complet
            center_x = self.global_crop_x + crop_w // 2
            center_y = self.global_crop_y + crop_h // 2
            aspect_crop = crop_w / crop_h if crop_h else 0
            aspect_video = video_w / video_h if video_h else 0
            crop_percent_w = crop_w / video_w * 100
            crop_percent_h = crop_h / video_h * 100

            # Brint(f"🖐️ [PAN] Requête VLC: crop_geometry='{geom}'")
            # Brint(f"🔍 [STATE] Zoom actuel: {self.global_zoom_level:.2f}")
            # Brint(f"📐 [COMPARE] Aspect ratio → Crop: {aspect_crop:.2f} vs Video: {aspect_video:.2f}")
            # Brint(f"[TBD] 📏 Crop size: {crop_w}px x {crop_h}px")
            # Brint(f"📊 [VIEWPORT] % vidéo visible → {crop_percent_w:.1f}% largeur, {crop_percent_h:.1f}% hauteur")
            Brint(f"🎯 [CENTER] Centre actuel du cadre crop: ({center_x}px, {center_y}px)")




    def reset_crop(self):
        self.global_zoom_level = 1.0
        self.global_crop_x = 0
        self.global_crop_y = 0
        self.apply_crop()
        self.save_loops_to_file()

    def toggle_edit_zoom(self):
        self.edit_mode_zoom = not self.edit_mode_zoom
        state = "Zoom Edit ON" if self.edit_mode_zoom else "Zoom Edit OFF"
        self.console.config(text=state)
        Brint(f"[TBD] 🎛️ Mode édition zoom: {state}")  


    #zoom funcs
    def toggle_zoom_memory(self):
        """Toggle entre zoom sauvegardé et pas de zoom."""
        if not hasattr(self, 'zoom_toggled_on'):
            self.zoom_toggled_on = False

        if not self.zoom_toggled_on:
            # 🔵 Première fois : sauver l'état actuel
            self.saved_zoom_level = self.global_zoom_level
            self.saved_crop_x = self.global_crop_x
            self.saved_crop_y = self.global_crop_y
            Brint(f"[TBD] 💾 Zoom sauvegardé : {self.saved_zoom_level}, crop=({self.saved_crop_x}, {self.saved_crop_y})")

            # 🔄 Puis reset zoom
            self.global_zoom_level = 1.0
            self.global_crop_x = 0
            self.global_crop_y = 0
            self.zoom_toggled_on = True
            Brint("[TBD] 🔄 Zoom reset à 1.0x")
        else:
            # 🔙 Restaurer le zoom sauvegardé
            if self.saved_zoom_level is not None:
                self.global_zoom_level = self.saved_zoom_level
                self.global_crop_x = self.saved_crop_x
                self.global_crop_y = self.saved_crop_y
                Brint(f"[TBD] 🔙 Zoom restauré : {self.global_zoom_level}x, crop=({self.global_crop_x}, {self.global_crop_y})")
            self.zoom_toggled_on = False

        self.apply_crop()
    def reset_zoom_memory(self):
        """Double-click: forget saved zoom."""
        Brint("[TBD] 🗑️ Zoom mémoire réinitialisé.")
        self.saved_zoom_level = None
        self.saved_crop_x = None
        self.saved_crop_y = None
        self.global_zoom_level = 1.0
        self.global_crop_x = 0
        self.global_crop_y = 0
        self.apply_crop()




        #ZOOMVIDEO ENDS
    
    #GDRIVE CALLER
    
    def export_loop_and_upload_to_drive(self, repeat=False):
        if not hasattr(self, 'loop_start') or not hasattr(self, 'loop_end') or not hasattr(self, 'current_path'):
            Brint("[TBD] ❌ Impossible d'exporter : informations de loop manquantes.")
            return

        duration = self.loop_end - self.loop_start
        duration_sec = duration / 1000.0
        if repeat:
            duration_sec *= 10

        media_base_name = os.path.splitext(os.path.basename(self.current_path))[0]
        temp_dir = tempfile.gettempdir()
        export_path = os.path.join(temp_dir, f"temp_loop.wav")

        Brint(f"[TBD] 🎧 Export de la boucle : {self.loop_start:.2f} ms → {self.loop_end:.2f} ms → {export_path}")

        start_sec = self.loop_start / 1000.0

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-i", self.current_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "48000",
            "-ac", "2"
        ]

        if repeat:
            cmd += ["-filter_complex", "aloop=loop=9:size=1:start=0", "-map", "[a]"]

        cmd += [export_path]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            upload_loop_to_drive(export_path, media_base_name)
        finally:
            if os.path.exists(export_path):
                os.remove(export_path)
                Brint(f"[TEMP CLEANUP] Removed temporary GDrive export: {export_path}")
    
        
    # --- Fonction pour charger une boucle sauvegardée quand on clique ---
    def load_saved_loop(self, index):
        Brint(f"\n[LOAD LOOP] 🔁 Chargement boucle index={index}")
        self.reset_rhythm_overlay()

        self.subdivision_state.clear()
        if not hasattr(self, "confirmed_red_subdivisions"):
            self.confirmed_red_subdivisions = {}
        else:
            self.confirmed_red_subdivisions.clear()
        self.user_hit_timestamps.clear()  # Clearing raw user hits for the previous loop
        self.subdiv_last_hit_loop.clear() # Clearing which subdiv was hit in which pass of the old loop
        self.loop_pass_count = 0          # Resetting loop pass counter for the new loop
        Brint("[LOAD LOOP] Cleared persistent hit states for new loop.")

        
        if index < 0 or index >= len(self.saved_loops):
            Brint(f"[ERROR] Index de boucle invalide : {index}")
            return

        loop = self.saved_loops[index]
        Brint(f"[DEBUG] 🔍 Données loop chargée : {loop}")

        is_valid, reason = self.validate_loop_data(loop)
        if not is_valid:
            Brint(f"[ERROR] Loop invalide : {reason}")
            return

        # ⚙️ Reconstruction de l'objet LoopData
        Brint("[STEP] Création de LoopData depuis dictionnaire")
        self.current_loop = LoopData.from_dict(loop)
        self.loop_start = self.current_loop.loop_start
        self.loop_end = self.current_loop.loop_end
        self.auto_zoom_on_loop_markers(force=True)

        # Restore confirmed hits context if present
        ctx = loop.get("confirmed_hit_context", {})
        timestamps = ctx.get("timestamps", [])
        grid_mode = ctx.get("grid_mode")
        self.confirmed_red_subdivisions = {}
        for t in timestamps:
            idx = self.timestamp_to_subdiv_index(t, self.grid_times)
            if idx is not None:
                self.confirmed_red_subdivisions.setdefault(idx, []).append(t * 1000)
        if grid_mode:
            self.subdivision_mode = grid_mode

        hit_timestamps = loop.get("hit_timestamps")
        if hit_timestamps is not None:
            self.user_hit_timestamps = [(t / 1000.0, 0) for t in hit_timestamps]
            self.current_loop.hit_timestamps = hit_timestamps
            Brint(
                f"[NHIT] Loaded {len(hit_timestamps)} hit_timestamps from loop | {self.abph_stamp()}"
            )
        else:
            hit_timings = loop.get("hit_timings", [])
            self.user_hit_timestamps = [(t, 0) for t in hit_timings]
            self.current_loop.hit_timings = hit_timings

        if self.loop_start is None or self.loop_end is None:
            Brint("[ERROR] loop_start ou loop_end manquant après chargement")
            return
        Brint(f"[OK] Boucle chargée : A={self.loop_start} | B={self.loop_end}")

        # 🔍 Zoom visuel
        if "loop_zoom_ratio" in loop:
            self.loop_zoom_ratio = loop["loop_zoom_ratio"]
            Brint(f"[STEP] Zoom restauré à {self.loop_zoom_ratio}")
            self.set_zoom_range_from_loop(self.current_loop)
            # Brint(f"[DEBUG BET] GlobXa = {self.GlobXa}")
            Brint(f"[DEBUG BET] loop_start = {loop['loop_start']} ms")

        else:
            Brint("[WARN] Aucun loop_zoom_ratio trouvé dans la sauvegarde")

        # 🎵 Tempo
        self.tempo_bpm = getattr(self.current_loop, "tempo_bpm", 60.0)
        Brint(f"[SYNC] 🎵 tempo_bpm synchronisé : {self.tempo_bpm}")

        # 🔁 Reconstruit le contexte (grille, mapping, etc.)
        Brint("[STEP] Reconstruction du contexte boucle")
        self.rebuild_loop_context()
        # Apply persistent validated hits from the saved loop
        self.remap_persistent_validated_hits()
        self.associate_hits_to_subdivisions()
        self.update_subdivision_states()
        self.draw_rhythm_grid_canvas()

        # 🕓 Positionnement du playhead
        Brint("[STEP] Positionnement du playhead")
        self.set_playhead_time(self.loop_start)

        # 🖼️ Timeline UI
        Brint("[STEP] Rafraîchissement des éléments de timeline statique")
        self.refresh_static_timeline_elements()

        # 🏷️ Nom affiché
        Brint("[STEP] Mise à jour du nom affiché")
        self.set_selected_loop_name(loop.get("name", "Unnamed"), self.loop_start, self.loop_end, source="load_saved_loop")

        # 🎚️ Tempo UI
        Brint("[STEP] Mise à jour de l'UI tempo")
        self.update_tempo_ui_from_loop()

        Brint(f"[✅ DONE] Boucle '{self.current_loop.name}' chargée avec succès")
        Brint(f"[DEBUG] A={self.hms(self.loop_start)} | B={self.hms(self.loop_end)} | BPM={self.tempo_bpm}")
    def abloops_json_path(self):
        base = os.path.splitext(os.path.basename(self.current_path))[0]
        return os.path.join(os.path.dirname(self.current_path), f".{base}.abloops.json")


    # def save_loops_to_file(self):
        # if not hasattr(self, "current_path") or not self.current_path:
            # return
        # try:
            # path = self.abloops_json_path()
            # with open(path, "w", encoding="utf-8") as f:
                # json.dump(self.saved_loops, f, indent=2)
            # Brint(f"[TBD] 💾 Boucles sauvegardées dans {path}")
        # except Exception as e:
            # Brint(f"[TBD] ❌ Erreur sauvegarde boucles: {e}")


    def force_save_current_loop(self):
        if self.loop_start is None or self.loop_end is None:
            Brint(f"[FORCE SAVE] ❌ A ou B non défini : {self.loop_start} → {self.loop_end}")
            return

        if self.loop_end <= self.loop_start:
            Brint(f"[FORCE SAVE] ❌ B <= A : {self.loop_start} → {self.loop_end}")
            return

        name = self.current_loop.name if hasattr(self, "current_loop") else "loop"

        Brint(f"[FORCE SAVE] 💾 Sauvegarde forcée de la boucle : {name}")

        loop_data = self.build_loop_data(name)
        if not loop_data:
            Brint("[FORCE SAVE] ❌ Échec de création du loop_data")
            return

        # Remplace ou ajoute la boucle
        for i, loop in enumerate(self.saved_loops):
            if loop['name'] == name:
                self.saved_loops[i] = loop_data
                break
        else:
            self.saved_loops.append(loop_data)

        self.save_loops_to_file()
        self.console.config(text=f"💾 Boucle '{name}' sauvegardée automatiquement")



    def save_current_loop(self):
        if self.loop_start is None or self.loop_end is None:
            self.console.config(text="⚠️ A ou B non défini")
            Brint(f"[WARNING] Sauvegarde annulée : loop_start={self.loop_start}, loop_end={self.loop_end}")
            return

        if self.loop_end <= self.loop_start:
            self.console.config(text="⚠️ B doit être > A")
            Brint(f"[WARNING] Sauvegarde annulée : loop_start={self.loop_start}, loop_end={self.loop_end}")
            return

        top = Toplevel()
        top.title("Sauvegarder ou Remplacer une boucle")
        Brint("[SAVE LOOP] Fenêtre de sauvegarde ouverte")
        Label(top, text="Clique sur une boucle pour la remplacer, ou entre un nouveau nom:").pack(pady=5)
        listbox = Listbox(top, selectmode=SINGLE)
        listbox.pack(padx=10, pady=5)

        for loop in self.saved_loops:
            listbox.insert('end', loop['name'])

        def save_new_or_replace():
            Brint("[SAVE LOOP] Bouton Enregistrer cliqué")
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                name = self.saved_loops[index]['name']
                self.saved_loops[index] = self.build_loop_data(name)
                self.console.config(text=f"♻️ Boucle '{name}' remplacée")
                Brint(f"[SAVE LOOP] Boucle '{name}' remplacée (index {index})")
            else:
                name = simpledialog.askstring("Nom de la nouvelle boucle", "Nom de la nouvelle boucle:")
                if not name:
                    Brint("[SAVE LOOP] Aucun nom saisi – sauvegarde annulée")
                    return
                self.saved_loops.append(self.build_loop_data(name))
                self.console.config(text=f"✅ Boucle '{name}' sauvegardée")
                Brint(f"[SAVE LOOP] Boucle '{name}' ajoutée (nouvelle entrée)")

            self.save_loops_to_file()
            Brint(f"[SAVE LOOP] Sauvegarde écrite dans le fichier ({len(self.saved_loops)} boucles)")
            top.destroy()

        Button(top, text="Enregistrer", command=save_new_or_replace).pack(pady=5)
        self.refresh_static_timeline_elements()
        Brint(f"[SAVE LOOP] loop_start={self.loop_start} ms | loop_end={self.loop_end} ms")

    def delete_selected_loop(self):
        if not self.saved_loops:
            self.console.config(text="⚠️ Aucune boucle à supprimer")
            return
        top = Toplevel()
        top.title("Supprimer une boucle")
        Label(top, text="Sélectionne une boucle à supprimer:").pack(pady=5)
        listbox = Listbox(top, selectmode=SINGLE)
        listbox.pack(padx=10, pady=5)
        for loop in self.saved_loops:
            listbox.insert('end', loop['name'])

        def delete_choice():
            selection = listbox.curselection()
            if not selection:
                return
            index = selection[0]
            name = self.saved_loops[index]['name']
            del self.saved_loops[index]
            self.save_loops_to_file()
            self.console.config(text=f"🗑️ Boucle '{name}' supprimée")
            top.destroy()

        Button(top, text="Supprimer", command=delete_choice).pack(pady=5)

    
    def precise_jump(self, base_delta_sec):
        """Fait un jump fin, adapté selon l'état du snap."""
        if not self.snap_to_keyframes_enabled:
            delta_sec = base_delta_sec / 4
            Brint(f"[TBD] 🛠️ Precision Mode: Jump réduit à {delta_sec:.3f} sec")
        else:
            delta_sec = base_delta_sec

        self.jump(delta_sec)

    
    def toggle_snap_mode(self):
        """Active ou désactive le snapping automatique aux keyframes."""
        self.snap_to_keyframes_enabled = not self.snap_to_keyframes_enabled
        state = "Activé" if self.snap_to_keyframes_enabled else "Désactivé"
        Brint(f"[TBD] 🔀 Snap I-frame : {state}")
        if hasattr(self, 'console'):
            self.console.config(text=f"🔀 Snap I-frame : {state}")

    
    def load_file(self, path):
        """Recharge un fichier vidéo existant après reencodage."""
        if hasattr(self, 'player'):
            self.player.stop()
            media = self.instance.media_new(path)
            self.player.set_media(media)
            self.player.play()
            Brint(f"[TBD] 🔄 Nouveau fichier chargé : {path}")

    
    def find_locks_on_file(self, filepath):
        Brint(f"[TBD] 🔎 Recherche de verrous sur {filepath}")
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                for f in proc.info['open_files'] or []:
                    if f.path == filepath:
                        Brint(f"🔒 {proc.info['name']} (pid {proc.info['pid']}) verrouille {filepath}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def reframe_current_media(self):
        """Vérifie la densité des I-frames et reencode si nécessaire."""
        if not hasattr(self, 'current_path') or not self.current_path:
            Brint("[TBD] ❌ Aucun fichier chargé")
            if hasattr(self, 'console'):
                self.console.config(text="❌ Aucun fichier chargé")
            return

        self.console.config(text="📈 Vérification densité GOP...")
        self.check_keyframe_density_and_reencode(self.current_path)
        self.console.config(text="✅ Vérification/Reframing terminé")

    
    def check_keyframe_density_and_reencode(self, path, max_spacing_sec=0.14, scan_window_sec=1.0):
        """Scanne la densité des I-frames et reencode si elles sont trop espacées ou trop peu présentes."""
        keyframes = self.extract_keyframes_around(path, center_time_sec=scan_window_sec/2, window_sec=scan_window_sec)

        if len(keyframes) < 2:
            Brint("[TBD] ⚠️ Trop peu de keyframes détectées — reencodage forcé.")
            self.reencode_video(path)
            return

        spacings = [keyframes[i+1] - keyframes[i] for i in range(len(keyframes)-1)]
        max_spacing = max(spacings)

        Brint(f"[TBD] 📈 Espacement max entre I-frames : {max_spacing:.3f}s")

        if max_spacing > max_spacing_sec:
            Brint("[TBD] 🚨 GOP trop espacé — reencodage nécessaire.")
            self.reencode_video(path)
        else:
            Brint("[TBD] ✅ GOP ok, pas besoin de reencoder.")

    def reencode_video(self, path):
        """Reencode la vidéo pour forcer un GOP serré et recharge à la bonne position."""
        from tkinter import messagebox

        temp_output = path + ".temp.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-i", path,
            "-c:v", "h264_nvenc",
            "-preset", "p1",
            "-rc", "vbr",
            "-cq", "28",
            "-g", "3",
            "-keyint_min", "3",
            "-bf", "2",
            "-b_ref_mode", "middle",
            "-spatial_aq", "1",
            "-temporal_aq", "1",
            "-aq-strength", "8",
            "-movflags", "+faststart",
            "-c:a", "copy",
            temp_output
        ]

        try:
            subprocess.run(cmd, check=True)

            # 🔵 Sauvegarde du temps actuel
            current_time_ms = self.player.get_time() if hasattr(self, 'player') else 0
            Brint(f"[TBD] 💾 Temps actuel avant reframe : {current_time_ms} ms")

            if hasattr(self, 'player') and self.player.get_media():
                self.player.stop()
                self.player.set_media(None)

            # Confirmation utilisateur
            answer = messagebox.askyesno(
                "Remplacer le fichier ?", f"Voulez-vous écraser {path} avec la version optimisée ?"
            )

            if answer:
                time.sleep(0.5)
                os.replace(temp_output, path)
                Brint(f"[TBD] ✅ Fichier remplacé : {path}")
                if hasattr(self, 'console'):
                    self.console.config(text="✅ Reencodage effectué")

                # 🔥 Recharger le fichier et repositionner
                media = self.instance.media_new(path)
                self.player.set_media(media)
                self.player.play()
                Brint(f"[TBD] 🔄 Nouveau fichier chargé : {path}")

                # 🔥 Repositionnement au temps précédent
                def jump_back():
                    Brint(f"[TBD] 🎯 Retour à {current_time_ms} ms")
                    # self.jump_to_time(current_time_ms)
                    self.safe_jump_to_time(current_time_ms, source="reencode_video")

                self.root.after(500, jump_back)

            else:
                Brint("[TBD] ⏩ Remplacement annulé par l'utilisateur.")
                if hasattr(self, 'console'):
                    self.console.config(text="⏩ Remplacement annulé")

        except Exception as e:
            Brint(f"[TBD] ❌ Erreur reencodage : {e}")
            if hasattr(self, 'console'):
                self.console.config(text=f"❌ Erreur reencodage : {e}")

    def measure_jump_stabilization(self, target_time_ms):
        """Surveille le temps réel que met VLC à stabiliser sa lecture après un jump."""
        start_time = time.perf_counter()

        def check_stabilization():
            if not hasattr(self, 'player'):
                return

            current_time = self.player.get_time()
            delta = abs(current_time - target_time_ms)

            if delta <= 100:  # Tolérance de 100 ms
                elapsed = (time.perf_counter() - start_time) * 1000
                mode = "Précis (set_time)" if self.use_precise_seek else "Rapide (set_position)"
                msg = f"🕰️ Lag mesuré pour jump : {elapsed:.1f} ms ({mode})"
                Brint("[TBD]", msg)
                if hasattr(self, 'console'):
                    self.console.config(text=msg)
            else:
                self.root.after(10, check_stabilization)

        self.root.after(10, check_stabilization)


    def toggle_seek_mode(self):
        self.use_precise_seek = not self.use_precise_seek
        mode = "Précis (set_time)" if self.use_precise_seek else "Rapide (set_position)"
        self.console.config(text=f"🔄 Mode seek: {mode}")
        Brint(f"[TBD] 🔄 Mode seek: {mode}")

    def jump_to_time(self, milliseconds):
        
        self.last_seek_time = time.time()
        Brint(f"[JUMP_TO_TIME] 🕰️ Jump vers {milliseconds}ms à t={self.last_seek_time:.3f}")

        """Saute à un temps précis soit via set_time(), soit via set_position() selon configuration et mesure la stabilisation."""
        if not hasattr(self, 'use_precise_seek'):
            self.use_precise_seek = True  # Valeur par défaut si non définie

        target_time = int(milliseconds)
        self.last_jump_target_ms = target_time
        self.last_jump_time = time.time()

        Brint(f"[TBD] 🎯 Demande de jump vers {target_time} ms")

        if self.use_precise_seek:
            # self.player.set_time(target_time)
            self.safe_jump_to_time(target_time, source="jump_to_time")
        else:
            if hasattr(self, 'duration') and self.duration > 0:
                fraction = target_time / self.duration
                fraction = min(max(fraction, 0.0), 1.0)
                # self.player.set_position(fraction)
                self.safe_jump_to_time(fraction, source="Jump to time2")
            else:
                Brint("[TBD] ⚠️ Durée vidéo inconnue, set_position() impossible")
                return

    #  self.measure_jump_stabilization(target_time)


    def extract_keyframes_around(self, path, center_time_sec, window_sec=2.0):
        """Extrait précisément les timestamps des I-frames dans une fenêtre autour d'un timestamp donné."""
        import subprocess

        start_time = max(0, center_time_sec - window_sec / 2)
        duration = window_sec

        cmd = [
            "ffmpeg",
            "-ss", str(start_time),
            "-t", str(duration),
            "-i", path,
            "-vf", "showinfo",
            "-f", "null", "-"
        ]

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = result.stdout

            keyframes = []

            for line in output.splitlines():
                if "iskey:1 type:I" in line:
                    parts = line.split("pts_time:")
                    if len(parts) > 1:
                        timestamp_str = parts[1].split()[0]
                        timestamp = float(timestamp_str) + start_time
                        keyframes.append(timestamp)

            Brint(f"[TBD] ✅ Keyframes autour de {center_time_sec:.3f}s : {keyframes}")
            return keyframes

        except Exception as e:
            Brint(f"[TBD] ❌ Erreur extraction keyframes autour de {center_time_sec:.3f}s: {e}")
            return []

    def snap_to_closest_keyframe(self, original_time_sec, keyframes, max_snap_distance_sec=0.21):
        """Tente de snapper un temps donné à la keyframe la plus proche si elle est dans la limite de tolérance."""
        if not keyframes:
            return original_time_sec  # Pas de keyframes disponibles

        closest_keyframe = min(keyframes, key=lambda x: abs(x - original_time_sec))
        distance = abs(closest_keyframe - original_time_sec)

        if distance <= max_snap_distance_sec:
            Brint(f"[TBD] 🔄 Snap automatique de {original_time_sec:.3f}s vers {closest_keyframe:.3f}s (écart {distance*1000:.1f} ms)")
            return closest_keyframe
        else:
            Brint(f"[TBD] ⏩ Aucun snap : écart minimum {distance*1000:.1f} ms")
            return original_time_sec
                
            
            
    def extract_keyframes(self, path):
        """Extrait les timestamps (en secondes) des keyframes (I-frames) du fichier vidéo."""
        cmd = [
            "ffprobe",
            "-select_streams", "v:0",
            "-show_frames",
            "-show_entries", "frame=pkt_pts_time,best_effort_timestamp_time,pict_type",
            "-of", "csv",
            path
        ]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
            keyframes = []
            for line in output.splitlines():
                parts = line.strip().split(",")
                if len(parts) == 3 and parts[2] == "I":
                    time_sec = float(parts[1])
                    keyframes.append(time_sec)
            Brint(f"[TBD] ✅ {len(keyframes)} keyframes extraites")
            return keyframes
        except Exception as e:
            Brint(f"[TBD] ❌ Erreur extraction keyframes: {e}")
            return []


    
    
    def stop_ram_loop(self, _=None):
        """Arrête complètement la lecture RAM (audio + vidéo) et remet VLC normal."""
        if hasattr(self, 'ram_audio_clip_path') and self.ram_audio_clip_path and os.path.exists(self.ram_audio_clip_path):
            try:
                os.remove(self.ram_audio_clip_path)
                Brint(f"[RAM LOOP CLEANUP] Removed temp audio clip: {self.ram_audio_clip_path}")
            except Exception as e:
                Brint(f"[RAM LOOP CLEANUP ERROR] Failed to remove {self.ram_audio_clip_path}: {e}")
            self.ram_audio_clip_path = None

        # 🛑 Stop audio RAM si lancé
        try:
            import pygame
            if pygame.mixer.get_init():
                Brint("[RAM LOOP] Arrêt audio RAM...")
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception as e:
            Brint(f"[RAM LOOP] Erreur arrêt audio RAM : {e}")

        # 🎯 Clean des attributs RAM (original attributes, if any beyond path)
        # self.ram_audio_clip = None # If this was a Pygame object, it's handled by pygame.mixer.quit()
        self.ram_audio_start_time = None

        # 🔈 Remettre VLC audio actif
        if hasattr(self, "player"):
            try:
                self.player.audio_set_mute(False)
                Brint("[RAM LOOP] VLC audio réactivé.")
            except Exception as e:
                Brint(f"[RAM LOOP] Erreur réactivation VLC audio : {e}")

        # ✅ Log console
        if hasattr(self, "console"):
            self.console.config(text="⏹️ RAM loop stoppée")

    def start_ram_loop(self):
        """ Lance la lecture audio RAM + synchronisation. """
        import threading
        import pygame

        if not hasattr(self, 'loop_start') or not hasattr(self, 'loop_end') or self.loop_start is None or self.loop_end is None:
            Brint("[RAM LOOP] A ou B non défini, impossible de lancer RAM loop.")
            return

        audio_path = self.extract_audio_to_wav()
        if not audio_path:
            Brint("[RAM LOOP] Erreur extraction audio.")
            return

        self.ram_audio_clip_path = audio_path # Store the path for cleanup

        try:
            pygame.mixer.init(frequency=48000, channels=2)
            pygame.mixer.music.load(self.ram_audio_clip_path)
            pygame.mixer.music.play(loops=-1)  # 🔄 boucle infinie
            self.ram_audio_start_time = time.perf_counter()
            Brint("[RAM LOOP] Lecture audio RAM démarrée.")
            # 🛑 Mute VLC pendant la lecture RAM
            if hasattr(self, "player"):
                self.player.audio_set_mute(True)

        except Exception as e:
            Brint(f"[RAM LOOP] Erreur lecture audio : {e}")


    def extract_audio_to_wav(self):
        """ Extrait la boucle A-B en WAV temporaire. """
        import subprocess
        import os
        if not hasattr(self, 'tempdir'):
            self.tempdir = os.path.join(os.getcwd(), "temp")
            os.makedirs(self.tempdir, exist_ok=True)

        temp_audio_path = os.path.join(self.tempdir, "temp_loop_audio.wav")
        start_sec = self.loop_start / 1000.0
        duration_sec = (self.loop_end - self.loop_start) / 1000.0

        cmd = [
            "ffmpeg", "-y",
            "-i", self.current_path,
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "48000",
            "-ac", "2",
            temp_audio_path
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            Brint(f"[AUDIO] WAV temporaire extrait : {temp_audio_path}")
            return temp_audio_path
        except Exception as e:
            Brint(f"[AUDIO] Erreur extraction WAV : {e}")
            return None

    def update_threshold(self, val):
        self.threshold = float(val) / 100
        if hasattr(self, 'all_detected_notes'):
            self.refresh_note_display()



    def update_trim_label(self, val=None):
        
        buffer = self.taille_buffer_ms.get()
        self.trim_label.config(text=f"🪚 Buffer: {buffer} ms")

        if hasattr(self, "original_loop_end"):
            self.loop_end = self.original_loop_end - buffer
            self.set_playhead_time(self.loop_start)
    
    def reset_speed(self):
        self.speed_var.set(1.0)
        if hasattr(self, 'player'):
            self.player.set_rate(1.0)
            self.console.config(text="⏩ Vitesse réinitialisée à 1.0x")
            
    # === RATIONALISÉ ET RANGÉ : DEBUT DU __init__ ===
    
    
    

    def __init__(self, root, autoload_index=0, autoload_path=None):
        self.root = root
        # debug helpers
        self.pause_each_update = tk.BooleanVar(value=False)
        self.update_delay_ms_var = tk.IntVar(value=30)
        self.state_window = None
        self.flags_window = None
        self._debug_labels = {}

        #new timestamps on hits
        self.raw_hit_memory = defaultdict(list)

        self.user_hit_timestamps = []
        self.impact_strikes = []
        # self.persistent_validated_hit_timestamps = set()

        #new ph
        self._last_playhead_x = None
        self.after_id = None
        self.is_paused = False

        self.temp_loop_save_path = os.path.join(tempfile.gettempdir(), "temp_loop_autosave.json")
        atexit.register(self.cleanup_temp_loop)


        
        #harmony
        self.harmony_chord_display_mode = "chord"      # ou "degree"
        self.harmony_note_display_mode = "key"      # ou "rel_key", "rel_chord"
        

        
        #heatmap       
        self.subdivision_state = {}  # clé = subdivision id, valeur = 0, 1 ou 2
        self.subdiv_last_hit_loop = {}  # clé = subdivision id, valeur = numéro de la dernière boucle où elle a été frappée
        self.loop_pass_count = 0  # compteur de boucles AB passées
        self.selected_subdiv_index = None  # currently focused subdiv in editor
        self.selected_subdiv_timestamp = None  # timestamp of that subdiv in ms
       
        #zoom screen 
        self.in_zoom_mode = False
        self.global_zoom_level = 1.0
        self.global_crop_x = 0


        
        #affichage wrapper
        self.in_local_loop_mode = False
        self.in_forced_jump = False
        
        #master notes and co
        self.current_loop_master_notes = []

        #interpol alone slow mo
        self.loop_local_start_time = None  # Temps système au moment où la boucle locale commence
        self.loop_duration_s = None        # Durée de la boucle en secondes
        self.awaiting_vlc_resync = False   # Flag : en attente que VLC ait sauté et rejoue
        
        
        # Zoom ratio controlling the visible portion of the loop
        self.loop_zoom_ratio = 1.0

        
        import json
        #RHYTHMe grille
        self.subdivision_mode = "ternary12"  # valeurs possibles : see ALL_SUBDIVISION_MODES
        # index of current syllable set for each mode
        self.syllable_set_idx = {key: 0 for key in RHYTHM_SYLLABLE_SETS}
        self._grid_bounce_x = None
        self._grid_bounce_ts = 0
        self.grid_subdivs = []

        # Grid visibility toggles
        self.rhythm_grid_enabled = True
        self.harmony_grid_enabled = True



        
    #grille chords

        self.chord_sequence = []


    #counters
        self.update_count = 0
        self.draw_count = 0
        self.last_stat_time = time.time()
        self.last_loop_exit_time = 0
        self.loop_cycle_id = 0
        self.last_handled_loop_id = -1
        self.mode_bar_enabled = False
        self.one_bar_duration_ms = 0
        self.mode_bar_bars = 1

        


        
    #resize window
        self._resize_after_id = None  # Pour le throttle


        self.root.title("Python VLC Video Player")
        self.root.geometry("960x540")

        # === VLC SETUP ===
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.speed_var = tk.DoubleVar(value=1.0)

        # === TEMPO CONFIG ===
        self.tempo_bpm = 60.0
        self.tempo_ref = 120.0
        self.tap_times = []
        self.tempo_mode = 'binary'  # or 'ternary'
        self.tempo_resolution = 4

        # === INIT ZOOM ET GRID ===
        self.zoom_start = 0
        self.zoom_end = 1
        self.grid_visible = True
        self.grid_canvas = None

        # === LOOP & SPAM PROTECTION ===
        self.saved_loops = []
        self.timeline_saved_loop_tags = {}
        self.last_jump_timestamps = []
        self.spam_cooldown_ms = 300
        self.spam_mode_active = False
        self.spam_mode_start_time = 0
        self.force_playhead_time_until = 0

        # === BUFFER CONFIG ===
        self.taille_buffer_ms = tk.IntVar(value=0)


        self.root.bind_all("<Key>", self.debug_keypress)


        


        # === STRUCTURE UI ===
        self.controls_top = Frame(self.root)
        self.controls_top.pack(fill=X, side='top')
        self.controls_bottom = Frame(self.root)
        self.controls_bottom.pack(fill=X, side='top')

        self.video_area = Frame(self.root)
        self.video_area.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.video_area, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        #harmony UI
        self.harmony_canvas = tk.Canvas(self.root, height=30, bg="#222")
        self.harmony_canvas.pack(fill="x", side="top", after=self.grid_canvas)


        # === GRID FRAME ===
        self.grid_frame = Frame(self.root)
        self.grid_frame.pack(side='top', fill='x')
        self.grid_toggle_button = Button(self.grid_frame, text='Grille ▼', command=self.toggle_grid)
        self.grid_toggle_button.pack(fill='x')
        self.grid_canvas = Canvas(self.grid_frame, height=20, bg='white')
        self.grid_canvas.pack(fill='x')

        # === TIMELINE FRAME ===
        self.timeline_frame = Frame(self.video_area)
        self.timeline_frame.pack(side='bottom', fill='x')
        self.timeline = Canvas(self.timeline_frame, height=24, bg='grey')
        self.timeline.pack(fill='x')
        # === TEMPO UI ===
        self.tempo_frame = Frame(self.controls_top)
        self.tempo_frame.pack(side='right', padx=10)

        Label(self.tempo_frame, text="🎼 Tempo").pack(side=LEFT)

        # Boutons +/- dans frame vertical compact
        self.tempo_buttons_frame = Frame(self.tempo_frame, width=15, height=20)
        self.tempo_buttons_frame.pack_propagate(False)
        self.tempo_buttons_frame.pack(side='left', padx=2)

        self.tempo_up_btn = Button(self.tempo_buttons_frame, text="+", command=self.increase_tempo)
        self.tempo_up_btn.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        self.tempo_down_btn = Button(self.tempo_buttons_frame, text="-", command=self.decrease_tempo)
        self.tempo_down_btn.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # Champ tempo à droite des boutons
        self.tempo_var = tk.DoubleVar(value=self.tempo_bpm)
        self.tempo_entry = tk.Entry(self.tempo_frame, textvariable=self.tempo_var, width=5, state="readonly")
        self.tempo_entry.pack(side=LEFT)
        self.tempo_entry.bind("<FocusIn>", self._enable_tempo_edit)
        self.tempo_entry.bind("<Return>", self._on_tempo_enter)
        self.tempo_entry.bind("<Button-1>", self._on_tempo_click)


        tempo_menu_button = tk.Menubutton(self.tempo_frame, text="⚙️ Édition Tempo", relief=tk.RAISED)
        tempo_menu = tk.Menu(tempo_menu_button, tearoff=0)

        # Fonctions déjà présentes
        tempo_menu.add_command(label="🫰 Tap Tempo", command=self.tap_tempo)
        tempo_menu.add_command(label="🎯 Tempo A–B", command=self.set_tempo_from_loop)
        tempo_menu.add_command(label="🔍 Analyse Boucle", command=self.analyser_boucle)

        # Multiplicateurs
        tempo_menu.add_separator()
        tempo_menu.add_command(label="×2", command=lambda: self.modify_tempo(factor=2))
        tempo_menu.add_command(label="÷2", command=lambda: self.modify_tempo(factor=0.5))
        tempo_menu.add_command(label="×3", command=lambda: self.modify_tempo(factor=3))
        tempo_menu.add_command(label="÷3", command=lambda: self.modify_tempo(factor=1/3))

        tempo_menu_button.config(menu=tempo_menu)
        tempo_menu_button.pack(side=LEFT, padx=5)

        self.lock_tempo_var = tk.BooleanVar(value=False)
        Checkbutton(self.tempo_frame, text="🔒 Lock", variable=self.lock_tempo_var, command=self.update_video_speed_from_tempo).pack(side=LEFT)
        self.tempo_label = Label(self.controls_bottom, text="")
        self.tempo_label.pack(side='right', padx=10)

        # === INIT UI SECTIONS SUPPLÉMENTAIRES ===
        self.console = Label(self.controls_bottom, text="", anchor=W)
        self.console.pack(side=LEFT, fill=X, expand=True)
        self.time_display = Label(self.controls_bottom, text="", anchor=W)
        self.time_display.pack(side=LEFT, padx=10)

        # self.power_btn removed (unused)
                
        #quickopen
        self.load_recent_files()


        # === INIT FLAGS & VARS ===
        self.playhead_id = None

        self.threshold = 0.5
        self.beat1 = None
        self.beat1_locked = False
        self.loop_start = self.loop_end = None
        self.grid_times = []
        self.grid_labels = []
        self.duration = 0
        self.step_mode_index = 0
        self.autostep_enabled = False
        self.beat1_candidates = []
        self.playhead_time = None
        self.use_precise_seek = True
        self.edit_mode = StringVar(value="playhead")
        self.snap_to_keyframes_enabled = False
        self.debug_show_beat_lines_only = False  
        self.debug_show_grid_lines = True
        self.GlobApos= None
        # self.GlobXa = None
        self.GlobXb = None
        self.needs_refresh = True
        self.cached_width = None
        self.awaiting_vlc_jump = False
        self.freeze_interpolation = False
        self.last_seek_time = 0



        
        # === DEMARRAGE ===
        self.root.after(100, self.update_loop)
        self.safe_update_playhead(0, source="INIT")
        self.force_playhead_time = False
        self.last_jump_target_ms = 0
        self.ram_audio_start_time = None

        # === RESULT BOX ===
        self.result_visible = False  # doit être AVANT le pack

        self.result_frame = Frame(self.root)

        self.result_box = tk.Text(self.result_frame,
                                  height=14,
                                  bg='black',
                                  fg='white',
                                  font=("Courier New", 16),
                                  takefocus=0,
                                  cursor='arrow')
        self.result_box.pack(fill=tk.BOTH, expand=True)

        # ❌ Supprime cette ligne :
        # self.result_frame.pack(fill=tk.BOTH, expand=True)

        # ✅ Ne pack que si visible :
        if self.result_visible:
            self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_box.bind("<Button-1>", self.on_result_click)
        self.result_box.config(state='disabled')

        # === CONTROLS PRINCIPAUX ===

        # === MENUS ET CONTRÔLES BOTTOM ===
        self.loop_length_var = tk.IntVar(value=2)  # 2 mesures par défaut
        # loop_length_menu removed (unused)

        self.label_subdivision = Label(self.controls_bottom, text="Subdivision: -", width=18)
        self.label_subdivision.pack(side=LEFT)

        # self.conf_slider removed (unused)

        self.beat1_selector_var = tk.StringVar(value="Beat 1")
        self.beat1_selector = tk.OptionMenu(self.controls_bottom, self.beat1_selector_var, "Beat 1")
        self.beat1_selector.pack(side=LEFT)

        #OPEN MENU
        control_buttons = [
            ("📂", lambda: self.show_open_menu(), "Ouvrir un fichier"),
        ]
        for txt, cmd, tip in control_buttons:
            btn = Button(self.controls_top, text=txt, command=cmd, width=5)
            btn.pack(side=LEFT)
            ToolTip(btn, tip)

        #LOOP MENU
        self.loop_menu_button = tk.Menubutton(self.controls_top, text="🔁 Boucle", relief=tk.RAISED)
        self.loop_menu = tk.Menu(self.loop_menu_button, tearoff=0)
        self.loop_menu_button.config(menu=self.loop_menu)
        self.loop_menu_button.pack(side=LEFT, padx=5)
        ToolTip(self.loop_menu_button, "Actions liées aux boucles et à leur analyse")
        self.interp_var = tk.BooleanVar(value=True)
        self.interp_chk = Checkbutton(self.controls_top, text="Interp", variable=self.interp_var)
        self.interp_chk.pack(side=LEFT)
        ToolTip(self.interp_chk, "Interpolation A/B")
        # === BOUTONS A / B ===
        self.btn_edit_A = Button(self.controls_top, text="A", command=lambda: self.set_edit_mode("loop_start"), width=3)
        self.btn_edit_A.pack(side=LEFT)
        ToolTip(self.btn_edit_A, "Éditer A")

        self.btn_edit_B = Button(self.controls_top, text="B", command=lambda: self.set_edit_mode("loop_end"), width=3)
        self.btn_edit_B.pack(side=LEFT)
        ToolTip(self.btn_edit_B, "Éditer B")
        #OPEN MENU 2/2
        control_buttons = [
            ("▶️", self.toggle_playpause_icon, "Lecture/Pause"),
        ]
        for txt, cmd, tip in control_buttons:
            btn = Button(self.controls_top, text=txt, command=cmd, width=5)
            btn.pack(side=LEFT)
            ToolTip(btn, tip)
        # Step menu removed (unused)
        

        # === BOUTON RÉSULTATS ===
        self.toggle_result_btn = Button(self.controls_bottom, text="🔽", command=self.toggle_result_box, width=3)
        self.toggle_result_btn.pack(side=LEFT)

        ToolTip(self.toggle_result_btn, "Afficher/masquer les résultats")

        # --- Ajout bouton pour vérifier/reencoder GOP ---




        #zoom screen button         
        self.zoom_menu_button = tk.Menubutton(self.controls_top, text="🔍 Zoom", relief=tk.RAISED)
        self.zoom_menu = tk.Menu(self.zoom_menu_button, tearoff=0)
        self.build_screen_zoom_menu(self.zoom_menu)
        self.zoom_menu_button.config(menu=self.zoom_menu)
        self.zoom_menu_button.pack(side=tk.LEFT, padx=5)


        # Fonctions de zoom et navigation
        # zoom_menu.add_command(label="🔍+ Zoom avant", command=self.zoom_in)
        # zoom_menu.add_command(label="🔎− Zoom arrière", command=self.zoom_out)
        # zoom_menu.add_separator()
        # zoom_menu.add_command(label="⬅️ Déplacer à gauche", command=self.pan_left)
        # zoom_menu.add_command(label="➡️ Déplacer à droite", command=self.pan_right)
        # zoom_menu.add_separator()
        # zoom_menu.add_command(label="🔄 Réinitialiser", command=self.reset_crop)

        # zoom_menu_button.config(menu=zoom_menu)
        # zoom_menu_button.pack(side=LEFT, padx=5)
        # ToolTip(zoom_menu_button, "Zoom et navigation horizontale")

            
            
         
        # ZOOMVIDEO
        self.saved_loops = []
        self.timeline_saved_loop_tags = {}
        self.global_zoom_level = 1.0
        self.global_crop_x = 0
        self.global_crop_y = 0
        self.zoom_step = 0.1
        self.pan_step = 50
        self.edit_mode_zoom = False  
        self.saved_zoom_level = None
        self.saved_crop_x = None
        self.saved_crop_y = None


        # Création du cadre vidéo dans le canvas
        self.video_frame = Frame(self.canvas, width=1920, height=1080)
        self.video_frame.pack()
        self.video_frame.place(x=0, y=0)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(self.video_frame.winfo_id())


        
        # === TIMELINE EVENTS
        self.edit_mode = StringVar(value="playhead")

        # === RHYTHM CONTROLS FRAME ===
        self.rhythm_controls_frame = Frame(self.controls_top)
        self.rhythm_controls_frame.pack(side='left', padx=5)

        # Zoom ratio selection
        self.zoom_ratio_var = tk.DoubleVar(value=self.loop_zoom_ratio)
        self.zoom_auto_code = -1.0  # special value meaning "4s"

        self.zoom_radio_frame = Frame(self.rhythm_controls_frame)
        self.zoom_radio_frame.pack(side='left')

        zoom_options = [
            (0.5, "0.5x"),
            (1.0, "1x"),
            (self.zoom_auto_code, "4s"),
        ]
        for val, label in zoom_options:
            rb = tk.Radiobutton(
                self.zoom_radio_frame,
                text=label,
                variable=self.zoom_ratio_var,
                value=val,
                indicatoron=0,
                width=3,
                command=self.on_zoom_ratio_change,
            )
            rb.pack(side='left')

        # Grid visibility toggles
        self.grid_toggle_frame = Frame(self.rhythm_controls_frame)
        self.grid_toggle_frame.pack(side='left', padx=5)

        self.show_rhythm_var = tk.BooleanVar(value=self.rhythm_grid_enabled)
        cb_rhythm = Checkbutton(
            self.grid_toggle_frame,
            text="Rhythm",
            variable=self.show_rhythm_var,
            command=self.update_rhythm_grid_visibility,
        )
        cb_rhythm.pack(side='left')

        self.show_harmony_var = tk.BooleanVar(value=self.harmony_grid_enabled)
        cb_harmony = Checkbutton(
            self.grid_toggle_frame,
            text="Harmony",
            variable=self.show_harmony_var,
            command=self.update_harmony_grid_visibility,
        )
        cb_harmony.pack(side='left')
        
        
        # === BINDINGS CLAVIER PRINCIPAUX ===
        #note display
        self.root.bind("<Shift-Tab>", lambda e: self.cycle_note_display_mode())

        
        #quicksave
        self.root.bind("<Control-s>", self.quick_save_current_loop)
        self.root.bind("<Control-z>", self.restore_loops_from_backup)
        self.root.bind("<Shift-S>", self.reload_current_loop)
        self.root.bind("<Control-p>", self.toggle_mode_bar)
        self.root.bind("<asterisk>", self.increase_mode_bar_bars) # '*' key
        self.root.bind("<slash>", self.decrease_mode_bar_bars)   # '/' key

        
        #heatmap
        self.root.bind("<period>", lambda e: self.reset_syllabic_grid_hits())
        self.root.bind_all("[", lambda e: self.offset_red_subdivisions(-1))
        self.root.bind_all("]", lambda e: self.offset_red_subdivisions(+1))

        
        #zoom bindings screen
        
        self.root.bind_all('<Key>', self.handle_screen_zoom_keypress)
        # self.root.bind("<Shift-Tab>", lambda e: self.cycle_subdivision_mode_backward())
        self.root.bind("<Shift-F1>", lambda e: self.cycle_subdivision_mode_backward())
        self.root.bind("<Shift-F2>", lambda e: self.cycle_subdivision_mode())
        self.loop_menu_button.bind("<Button-1>", lambda e: self.update_loop_menu())
        # self.root.bind("<F4>", self.edit_current_chord_from_playhead)
        self.root.bind("<F4>", self.toggle_state_window)
        self.root.bind("<F1>", lambda e: self.cycle_syllable_set_backward())
        self.root.bind("<F2>", lambda e: self.cycle_syllable_set())
        self.root.bind("<F3>", lambda e: self.open_debug_flags_window())
        
        self.root.bind("<F10>", self.start_profiling_5s)
        self.root.bind("<=>", lambda e: self.open_chord_editor_all())
        # self.root.bind("<F9>", self.dump_playhead_debug_log())

        self.root.bind('<F9>', lambda e: self.dump_playhead_debug_log())
        self.root.bind('<space>', lambda e: self.toggle_pause())
        # self.root.bind('<Right>', lambda e: self.jump(10))
        # self.root.bind('<Left>', lambda e: self.jump(-10))
        # self.root.bind('<Shift-Right>', lambda e: self.jump(1))
        # self.root.bind('<Shift-Left>', lambda e: self.jump(-1))
        # self.root.bind('<Control-Right>', lambda e: self.jump(60))
        # self.root.bind('<Control-Left>', lambda e: self.jump(-60))
        # self.root.bind('<Alt-Right>', lambda e: self.jump(600))
        # self.root.bind('<Alt-Left>', lambda e: self.jump(-600))
        # self.root.bind('<Control-Shift-Right>', lambda e: self.precise_jump(0.1))
        # self.root.bind('<Control-Shift-Left>', lambda e: self.precise_jump(-0.1))
        self.root.bind("<Left>", lambda e: self.jump_playhead(-1, "beat"))
        self.root.bind("<Right>", lambda e: self.jump_playhead(+1, "beat"))
        self.root.bind("<Shift-Left>", lambda e: self.jump_playhead(-1, "8th"))
        self.root.bind("<Shift-Right>", lambda e: self.jump_playhead(+1, "8th"))
        self.root.bind("<Control-Left>", lambda e: self.jump_playhead(-1, "bar"))
        self.root.bind("<Control-Right>", lambda e: self.jump_playhead(+1, "bar"))
        self.root.bind("<Control-Shift-Left>", lambda e: self.jump_playhead(-1, "16th"))
        self.root.bind("<Control-Shift-Right>", lambda e: self.jump_playhead(+1, "16th"))
        self.root.bind("<Alt-Control-Shift-Left>", lambda e: self.jump_playhead(-1, "64th"))
        self.root.bind("<Alt-Control-Shift-Right>", lambda e: self.jump_playhead(+1, "64th"))
        self.root.bind("r", lambda e: self.replay_from_A())
        self.timeline.bind("<Button-1>", self.on_timeline_click)
        self.timeline.bind("<B1-Motion>", self.on_timeline_drag)
        self.timeline.bind("<Configure>", self.on_timeline_resize)




        self.root.bind('<Key-q>', lambda e: self.cycle_chord_harmony_mode())
        self.root.bind('<Shift-Q>', lambda e: self.cycle_note_harmony_mode())
        self.root.bind('<Key-plus>', lambda e: self.adjust_speed(0.1))
        self.root.bind('<Key-minus>', lambda e: self.adjust_speed(-0.1))
        self.root.bind('<Up>', lambda e: self.adjust_volume(10))
        self.root.bind('<Down>', lambda e: self.adjust_volume(-10))
        self.root.bind('<Key-a>', lambda e: self.set_edit_mode("loop_start"))
        self.root.bind('<Key-b>', lambda e: self.set_edit_mode("loop_end"))
        self.root.bind('<Control-Return>', lambda e: self.reset_speed())
        self.root.bind('<Key-s>', lambda e: self.stop_and_return())
        self.root.bind("<Shift-A>", lambda e: self.jump_to_A())
        # self.root.bind('<Key-r>', lambda e: self.toggle_loop())
        self.root.bind('<Shift-T>', lambda e: self.toggle_autostep())
        self.root.bind('<Key-t>', lambda e: self.step_play())
        self.root.bind('<Shift-A>', lambda e: self.record_loop_marker("loop_start", auto_exit=True))
        self.root.bind('<Shift-B>', lambda e: self.record_loop_marker("loop_end", auto_exit=True))
        self.root.bind("<Shift-C>", self.clear_loop)
        self.root.bind('<Key-l>', lambda e: self.analyser_boucle())
        self.root.bind('<Key-l>', lambda e: self.analyser_boucle())
        self.root.bind('<Key-h>', lambda e: self.load_hotspot_candidates())
        self.root.bind('<Key-m>', lambda e: self.place_marker())
        self.root.bind('<Shift-M>', lambda e: self.remove_last_marker())
        self.root.bind('<Key-Escape>', lambda e: self.clear_edit_mode())
        self.root.bind('<Key-c>', lambda e: self.center_on_playhead())
        self.root.bind('<Shift-O>', lambda e: self.start_ram_loop())
        self.root.bind('<Shift-P>', lambda e: self.stop_ram_loop())

        # Charger le zoom précédent si existant
        # self.load_screen_zoom_prefs()
        self.try_auto_load_recent_file(autoload_index, autoload_path)
    
    def replay_from_A(self):
        if self.loop_start:
            Brint("[PH R] 🔁 Touche R → retour à A")
            self.safe_jump_to_time(self.loop_start, source="Touche R")
            self.player.play()
            self.console.config(text="▶️ Relecture depuis A")
            self.last_loop_jump_time = time.perf_counter()
            Brint("[PH LOOPJUMP] 🔁 last_loop_jump_time resynchronisé après retour à A via R")


    
    def clear_edit_mode(self):
        self.edit_mode.set("")
        self.console.config(text="🛑 Mode édition désactivé")
    
    def toggle_playpause_icon(self):
        self.playhead_time = None  # ✅ efface toute position forcée une fois la lecture lancée

        if self.player.is_playing():
            self.player.pause()
            self.playpause_btn.config(text="▶️")
        else:
            self.player.play()
            self.playpause_btn.config(text="⏸")

    def adjust_speed(self, delta):
        rate = self.player.get_rate()
        new_rate = max(0.1, min(4.0, rate + delta))
        self.player.set_rate(new_rate)
        self.console.config(text=f"⏩ Vitesse : x{new_rate:.1f}")

    def adjust_volume(self, delta):
        vol = self.player.audio_get_volume()
        self.player.audio_set_volume(min(max(0, vol + delta), 200))
        self.console.config(text=f"🔊 Volume : {self.player.audio_get_volume()}")

    def stop_and_return(self):
        self.player.stop()
        if self.loop_start:
            self.set_playhead_time(self.loop_start)
        else:
            self.set_playhead_time(0)
        self.console.config(text="⏹ Retour au début")

    def toggle_loop(self):
        state = self.player.get_state()
        self.autostep_enabled = not self.autostep_enabled
        self.console.config(text=f"🔁 Lecture en boucle : {'ON' if self.autostep_enabled else 'OFF'}")
        

    def center_on_playhead(self):
        # À ajuster selon ton implémentation timeline
            self.console.config(text="🎯 Centering not implemented (à brancher)")
    def on_result_click(self, event):
        def handle_click():
            if getattr(self, "_double_click_detected", False):
                self._double_click_detected = False
                return  # ⛔ Ignore le simple-clic si double-clic

            # Récupération du timestamp dans la ligne
            index = self.result_box.index(f"@{event.x},{event.y}")
            line_index = index.split(".")[0]
            line_content = self.result_box.get(f"{line_index}.0", f"{line_index}.end")

            try:
                timestamp_str = line_content.strip().split()[0]
                timestamp = hms_to_seconds(timestamp_str)
                ms = int(timestamp * 1000)
            except (IndexError, ValueError):
                Brint(f"[WARNING TIMESTAMP] ❌ Timestamp invalide : '{line_content}'")
                return

            self.playhead_time = timestamp  # seconds

            was_playing = self.player.is_playing()

            # Stop + reload
            self.player.stop()
            if hasattr(self, "current_path"):
                self.media = self.instance.media_new(self.current_path)
                self.player.set_media(self.media)
                self.player.set_hwnd(self.canvas.winfo_id())

            def seek_then_restore():
                # self.jump_to_time(ms)
                self.safe_jump_to_time(ms, source="seek_then_restore")
                self.safe_update_playhead(ms, source="seek_then_restore")
                # self.time_display.config(text=f"⏱ {self.hms(ms)} / {self.hms(self.duration)}")

                self.playhead_time = ms / 1000
                if was_playing:
                    self.player.play()
                    Brint(f"[TBD] ▶️ Lecture relancée à {ms} ms")
                else:
                    self.player.play()
                    self.root.after(100, self.player.pause)  # pause après init lecture
                    Brint(f"[TBD] ⏸ Pause appliquée à {ms} ms")

            # Lecture forcée nécessaire pour initialiser le player
            self.player.play()
            self.root.after(100, seek_then_restore)

            Brint(f"[TBD] 🎯 Jump to {timestamp:.3f}s depuis résultat d’analyse.")

        self.root.after(200, handle_click)



    def refresh_note_display(self):
        if not hasattr(self, "all_detected_notes"):
            self.console.config(text="⛔ Aucune analyse disponible")
            return

        notes_display = []
        degres_display = []

        def midi_to_pitch_number(note):
            try:
                return pretty_midi.note_name_to_number(note)
            except:
                return 128

        for i in range(len(self.grid_times)):
            group = self.all_detected_notes[i] if i < len(self.all_detected_notes) else []
            raw_filtered = [(n, c) for n, c in group if c >= self.threshold]

            # Filtrage : une seule note par nom exact (A4), la plus confiante
            pitch_conf_map = {}
            for note, conf in raw_filtered:
                if note not in pitch_conf_map or conf > pitch_conf_map[note]:
                    pitch_conf_map[note] = conf

            # Regrouper par lettre fondamentale (A-G), garder la plus grave
            from collections import defaultdict

            def midi_to_pitch_number(note):
                try:
                    return pretty_midi.note_name_to_number(note)
                except:
                    return -1  # valeur basse pour éviter qu'un nom invalide passe

            group = self.all_detected_notes[i] if i < len(self.all_detected_notes) else []
            raw_filtered = [(n, c) for n, c in group if c >= self.threshold]

            # Étape 1 : garder la note la plus confiante par nom exact (ex: A4)
            pitch_conf_map = {}
            for note, conf in raw_filtered:
                if note not in pitch_conf_map or conf > pitch_conf_map[note]:
                    pitch_conf_map[note] = conf

            # Étape 2 : filtrer une seule note par lettre (A-G), garder la plus aiguë
            letter_dict = {}
            for note, conf in pitch_conf_map.items():
                letter_match = re.match(r"[A-Ga-g]", note)
                if not letter_match:
                    continue
                letter = letter_match.group(0).upper()
                if letter not in letter_dict:
                    letter_dict[letter] = (note, conf)
                else:
                    prev_note = letter_dict[letter][0]
                    if midi_to_pitch_number(note) > midi_to_pitch_number(prev_note):
                        letter_dict[letter] = (note, conf)

            filtered = sorted(letter_dict.values(), key=lambda x: -x[1])

            if filtered:
                note_str = ", ".join(f"{n} ({c:.2f})" for n, c in filtered)
                degree_note = filtered[0][0]
            else:
                note_str = "-"
                degree_note = None

            notes_display.append(note_str)
            degres_display.append(degree_note)

        self.result_box.config(state='normal')
        self.result_box.delete('1.0', tk.END)
        mode = getattr(self, "subdivision_mode", "inconnu")
        self.result_box.insert(tk.END, f"🎼 Analyse RHYTHMique : {mode}\n")


        self.result_box.insert(tk.END, f"{'Timestamp':10} {'Temps':10} {'Musc':5} {'Notes détectées':40} {'Accord':8} {'Degré'}\n")
        total_steps = len(self.grid_labels)
        subdivision_mode = getattr(self, "subdivision_mode", None)

        subdivs_per_beat = self.get_subdivisions_per_beat(subdivision_mode)


        steps_per_bar = 4 * subdivs_per_beat
        total_bars = (total_steps + steps_per_bar - 1) // steps_per_bar
        if not hasattr(self, "chord_sequence") or not self.chord_sequence:
            self.chord_sequence = []
            chords = self.current_loop.chords
            for chord in chords:
                self.chord_sequence.append((
                    chord.get("chord", "?"),
                    chord.get("degree", "?")
                ))
            Brint(f"[DEBUG] chord_sequence régénérée depuis current_loop.chords ({len(self.chord_sequence)} accords)")

        accords = self.chord_sequence[:total_bars]
        


        Brint(f"[DEBUG] accords utilisés : {accords[:4]}...")

        min_len = min(len(self.grid_labels), len(self.grid_times), len(notes_display))

        for i in range(min_len):
            t = self.grid_times[i]
            timestamp = self.hms(t * 1000)
            note_str = notes_display[i]
            deg_note = degres_display[i]
            deg_name = re.match(r"^[A-Ga-g#b]+", deg_note).group(0) if deg_note else None

            bar_index = i // steps_per_bar
            beat_in_bar = (i % steps_per_bar) // subdivs_per_beat
            pos_in_beat = (i % steps_per_bar) % subdivs_per_beat

            acc, root = accords[bar_index]
            deg = interval_to_degree(deg_name, normalize_root(root)) if deg_name else "-"
            try:
                acc, root = accords[bar_index]
            except IndexError:
                acc, root = "?", "?"
                Brint(f"[WARN] Accord manquant pour bar_index={bar_index}, fallback")

            if self.subdivision_mode == "binary8":
                musical = str(beat_in_bar + 1) if pos_in_beat == 0 else "n"
            elif self.subdivision_mode == "binary16":
                musical = str(beat_in_bar + 1) if pos_in_beat == 0 else ["y", "&", "a", "n"][(pos_in_beat - 1) % 4]
            elif self.subdivision_mode in ("ternary8", "ternary12"):
                musical = [str(beat_in_bar + 1), "T", "L"][pos_in_beat]
            elif self.subdivision_mode in ("ternary16", "ternary24"):
                musical = str(beat_in_bar + 1) if pos_in_beat == 0 else ["t", "l", "n", "t", "l"][pos_in_beat - 1]
            elif self.subdivision_mode == "binary4":
                musical = str(beat_in_bar + 1)
            elif self.subdivision_mode == "ternary36":
                musical = str(beat_in_bar + 1) if pos_in_beat == 0 else [
                    "1", "2", "3", "4", "5", "6", "7", "8", "9"][pos_in_beat - 1]
            else:
                musical = "-"

            temps = f"{bar_index+1}.{beat_in_bar+1}.{pos_in_beat+1}"

            start_index = self.result_box.index(tk.END)
            self.result_box.insert(tk.END,
                f"{timestamp:10} {temps:10} {musical:5} {note_str:40} {acc:8} {deg}\n")

            # Remplace cette ligne par :
            harmo_index = self.result_box.index(f"{start_index} + {len(timestamp)+1+len(temps)+1+len(musical)+1}c")
            if "harmo:" in note_str:
                harmo_pos = note_str.index("harmo:")
                harmo_start = f"{start_index} + {note_str.index('harmo:') + 51}c"  # +51 to skip fixed-width prefix
                harmo_end = f"{start_index} lineend"
                self.result_box.tag_add("harmonics", harmo_start, harmo_end)

            # Puis une seule fois en bas de ta fonction :
            self.result_box.tag_config("harmonics", foreground="gray", font=("TkDefaultFont", 9, "italic")) 
        self.result_box.config(state='disabled')
            
        
        
        
    def set_edit_mode(self, mode):
        current = self.edit_mode.get()
        Brint(f"[TBD] 🎛️ set_edit_mode() : current={current}, requested={mode}")

        if current == mode:
            self.edit_mode.set("playhead")
            self.console.config(text="🎯 Mode : Playhead")
            Brint("[TBD] 🎯 Retour en mode playhead")
        else:
            self.edit_mode.set(mode)
            label = "A" if mode == "loop_start" else "B"
            self.console.config(text=f"✏️ Mode édition : {label}")
            Brint(f"[TBD] ✏️ Passage en mode édition {label}")

        # Keep focus on the main window so arrow keys work
        self.root.focus_set()

        if hasattr(self, "btn_edit_A") and hasattr(self, "btn_edit_B"):
            self.btn_edit_A.config(relief="sunken" if mode == "loop_start" else "raised")
            self.btn_edit_B.config(relief="sunken" if mode == "loop_end" else "raised")
    def toggle_result_box(self):
        if self.result_visible:
            self.result_frame.pack_forget()
            self.toggle_result_btn.config(text="🔼")
            self.result_visible = False
        else:
            self.result_frame.pack(fill=tk.BOTH, expand=False)
            self.toggle_result_btn.config(text="🔽")
            self.result_visible = True
    def record_marker(self):
        mode = self.edit_mode.get()
        if mode in ["loop_start", "loop_end"]:
            self.record_loop_marker(mode)

    def select_jamtrack_zone(self, label):
        index = int(label.split(" ")[1].replace(":", "")) - 1
        start, end, beat1 = self.jamtrack_zones[index]
        self.loop_start = int(start)
        self.loop_end = int(end )
        self.beat1 = beat1
        self.beat1_locked = True
        Brint(f"[TBD] 🎯 Jamtrack {label} sélectionnée – Beat 1 @ {self.hms(self.loop_start)}")
        self.analyser_boucle()

    def load_jamtrack_zones(self, path):
        self.console.config(text="🧠 Analyse jamtrack en cours...")

        # ou autre emplacement
        self.jamtrack_zones = detect_jamtrack_zones(path)
        options = []
        for i, (start, end, beat1) in enumerate(self.jamtrack_zones):
            label = f"Zone {i+1}: {self.hms(start)} → {self.hms(end)}"
            options.append(label)

        menu = self.beat1_selector["menu"]

        menu.delete(0, "end")
        for opt in options:
            menu.add_command(label=opt, command=lambda v=opt: self.select_jamtrack_zone(v))
        self.console.config(text=f"✅ {len(self.jamtrack_zones)} zones détectées")



    def toggle_autostep(self):
        self.autostep_enabled = not self.autostep_enabled
        state = "✅ AutoStep ON" if self.autostep_enabled else "⏹️ AutoStep OFF"
        self.console.config(text=state)
        if self.autostep_enabled:
            self.step_play()



    def update_playhead_by_time(self, forced_time_ms=None):
        Brint(f"[PH USE] 🧭 update_playhead_by_time() → temps utilisé = {forced_time_ms if forced_time_ms is not None else self.playhead_time * 1000:.1f} ms")

        if forced_time_ms is not None:
            current_time_ms = forced_time_ms
        else:
            current_time_ms = self.playhead_time * 1000

        if forced_time_ms is None and not self.player.is_playing():
            return

        self.update_count += 1
        if not self.duration or self.duration <= 0:
            return

        if self.cached_width is None or time.time() - self.last_width_update > 1:
            self.cached_width = self.timeline.winfo_width()
            self.last_width_update = time.time()
        width = self.cached_width
        if width <= 1:
            self.root.after(100, lambda: self.safe_update_playhead(current_time_ms, source="update_playhead_by_time"))
            return

        zoom = self.get_zoom_context()
        zoom_range = zoom["zoom_range"]
        if zoom_range <= 0:
            Brint(f"[ERROR] ❌ zoom_range invalide ({zoom_range}). Fallback full view.")
            zoom_start = 0
            zoom_end = self.duration / 1000.0
            zoom_range = zoom_end - zoom_start

        t_sec = current_time_ms / 1000.0
        x = self.time_sec_to_canvas_x(t_sec)
        Brint(f"[PH DRAW] ⏱ x = {x}px pour t = {t_sec:.3f}s")


        if self._last_playhead_x is not None and x < self._last_playhead_x:
            pass
        if x == self._last_playhead_x:
            self._draw_count_same_x += 1
        else:
            self._last_playhead_x = x
            self._draw_count_same_x = 1

        if self.playhead_id is None:
            self.playhead_id = self.timeline.create_line(x, 0, x, 24, fill="red", tags="playhead")
        else:
            self.timeline.coords(self.playhead_id, x, 0, x, 24)
        self.timeline.tag_raise(self.playhead_id)

        self.draw_count += 1
        self.GlobApos = x

        now = time.time()
        if now - self.last_stat_time > 0.03:
            ratio = (self.draw_count / self.update_count) if self.update_count else 0
            self.needs_refresh = True
            self.refresh_static_timeline_elements()
            self.update_count = 0
            self.draw_count = 0
            self.last_stat_time = now

        self.playhead_canvas_x = self.time_sec_to_canvas_x(current_time_ms / 1000.0) if zoom_range > 0 else -9999

        # -- New behavior: auto-adjust zoom as playhead moves --
        old_zoom = self.get_zoom_context()
        self.maybe_adjust_zoom_if_out_of_frame()
        new_zoom = self.get_zoom_context()
        if old_zoom != new_zoom:
            self.needs_refresh = True
        self.refresh_static_timeline_elements()

    def refresh_chord_editor(self):
        """Refresh highlight state in the chord editor based on subdivision_state."""
        if not getattr(self, "chord_editor_popup", None):
            return
        if not getattr(self, "chord_editor_note_entries", None):
            return
        if not self.chord_editor_popup.winfo_exists():
            return
        for idx, _, _, entry in self.chord_editor_note_entries:
            if self.subdivision_state.get(idx, 0) == 2:
                entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            else:
                entry.configure(highlightthickness=0)



    def refresh_static_timeline_elements(self):
        
        
        if not self.needs_refresh:
            return
        self.timeline.delete("loop_marker")
        self.timeline.delete("saved_loop")
        self.timeline.delete("audio_power")
        self.timeline_saved_loop_tags.clear()

        if self.cached_width is None or time.time() - self.last_width_update > 1:
            self.cached_width = self.timeline.winfo_width()
            self.last_width_update = time.time()
        width = self.cached_width
        if width <= 1 or not self.duration:
            return

        # ✅ Mise à jour propre via la fonction centrale
        # if self.loop_start and self.loop_end:
            # self.GlobXa, self.GlobXb = self.get_loop_zoom_range()
        # else:
            # self.GlobXa = 0
            # self.GlobXb = self.duration / 1000.0

        zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_end = zoom["zoom_end"]
        zoom_range = zoom["zoom_range"]

        if zoom_range <= 0:
            Brint(f"[ERROR] ❌ zoom_range invalide ({zoom_range}). Fallback full view.")
            # self.GlobXa = 0
            # self.GlobXb = self.duration / 1000.0
            zoom = self.get_zoom_context()
            zoom_start = zoom["zoom_start"]
            zoom_end = zoom["zoom_end"]
            zoom_range = zoom["zoom_range"]


        for idx, loop in enumerate(self.saved_loops):
            x_start = self.time_sec_to_canvas_x(loop['loop_start'] / 1000)
            # x_start = time_to_x(loop['loop_start'] / 1000)
            x_end = self.time_sec_to_canvas_x(loop['loop_end'] / 1000)
            # x_end = time_to_x(loop['loop_end'] / 1000)
            tag = f"saved_loop_{idx}"
            tags = ("saved_loop", tag)
            self.timeline.create_rectangle(x_start, 0, x_end, 24, outline="cyan", width=2, tags=tags)
            x_label = x_start + 5  # petit décalage optionnel pour éviter d'être collé sur la ligne A
            self.timeline.create_text(x_label, 6, text=loop["name"], anchor='w', fill="cyan", tags=tags)
            self.timeline.tag_bind(tag, "<Button-1>", lambda e, i=idx: self.load_saved_loop(i))

        if self.loop_start is not None:
            xa_raw = self.time_sec_to_canvas_x(self.loop_start / 1000)
            xa = min(max(0, xa_raw), width)
            anchor_a = 'w' if xa < width - 40 else 'e'
            offset_a = 10 if anchor_a == 'w' else -10
            self.timeline.create_line(xa, 0, xa, 24, fill="green", tags="loop_marker")
            text_a = (
                f"A: {self.hms(self.loop_start)}"
                if zoom_start <= self.loop_start <= zoom_end
                else "A"
            )
            self.timeline.create_text(
                xa + offset_a,
                18,
                text=text_a,
                anchor=anchor_a,
                fill="white",
                tags="loop_marker",
            )

        if self.loop_end is not None:
            xb_raw = self.time_sec_to_canvas_x(self.loop_end / 1000)
            xb = min(max(0, xb_raw), width)
            anchor_b = 'w' if xb < width - 40 else 'e'
            offset_b = 10 if anchor_b == 'w' else -10
            self.timeline.create_line(xb, 0, xb, 24, fill="orange", tags="loop_marker")
            text_b = (
                f"B: {self.hms(self.loop_end)}"
                if zoom_start <= self.loop_end <= zoom_end
                else "B"
            )
            self.timeline.create_text(
                xb + offset_b,
                18,
                text=text_b,
                anchor=anchor_b,
                fill="white",
                tags="loop_marker",
            )

        self.draw_audio_power_overlay()

        self.needs_refresh = False

    def draw_audio_power_overlay(self):
        if not hasattr(self, 'audio_power_data') or self.audio_power_data is None:
            return
        if getattr(self, 'audio_power_max', 0) == 0:
            self.audio_power_max = float(np.max(self.audio_power_data[1])) if len(self.audio_power_data[1]) else 0.0
        times, rms = self.audio_power_data
        zoom = self.get_zoom_context()
        start_ms = zoom['zoom_start']
        end_ms = zoom['zoom_end']
        mask = (times * 1000 >= start_ms) & (times * 1000 <= end_ms)
        times = times[mask]
        rms = rms[mask]
        if len(times) == 0:
            return
        bottom = 24

        height = bottom
        canvas_width = max(1, self.timeline.winfo_width())
        step = max(1, len(times) // canvas_width)
        points = []
        for t, r in zip(times[::step], rms[::step]):

            x = self.time_sec_to_canvas_x(t, use_margin=False)
            y = bottom - (r / self.audio_power_max) * height
            points.extend([x, y])
        if len(points) >= 4:

            poly = [points[0], bottom]
            for i in range(0, len(points), 2):
                poly.extend([points[i], points[i + 1]])
            poly.extend([points[-2], bottom])
            self.timeline.create_polygon(*poly, fill='#666', outline='', tags='audio_power')
            self.timeline.create_line(*points, fill='#666', width=1, tags='audio_power')
            self.timeline.tag_lower('audio_power')



    def load_hotspot_candidates(self):
        

        if not hasattr(self, 'current_path'):
            self.console.config(text="⚠️ Aucun fichier chargé")
            return

        self.console.config(text="🔥 Analyse hotspots en cours...")

        import threading
        threading.Thread(target=self._run_hotspot_analysis, daemon=True).start()

    def _run_hotspot_analysis(self):
        

        results = find_beat1_hotspots(self.current_path)
        self.beat1_candidates = results

        def update_menu():
            menu = self.beat1_selector["menu"]
            menu.delete(0, "end")
            for i, (start, end, beat1, tempo) in enumerate(results):
                label = f"{i+1}: {self.hms(start)} → {self.hms(end)} @ {int(tempo)} BPM"
                menu.add_command(label=label, command=lambda v=i: self.select_beat1_candidate(v))
            if results:
                self.beat1_selector_var.set("✅ Hotspot détecté")
                self.console.config(text=f"✅ {len(results)} hotspots détectés")
            else:
                self.beat1_selector_var.set("Aucun hotspot")
                self.console.config(text="❌ Aucun hotspot trouvé")

        self.root.after(0, update_menu)


    def load_beat1_candidates(self):
        if not hasattr(self, 'current_path'):
            self.console.config(text="⚠️ Aucun fichier chargé")
            return

        self.console.config(text="🔎 Analyse des count-ins en cours...")

        import threading
        threading.Thread(target=self._run_beat1_detection_from_scanfile, daemon=True).start()


    def _run_beat1_detection_from_scanfile(self):
        results = detect_countins_with_rms(self.current_path, strict=True, mode="classic-countin",verbose=False)
        
        self.beat1_candidates = []
        for g in results:
            start = g["clicks"][0]
            beat1 = g["beat1"]
            tempo = g["bpm_ternary"] * 3  # ⬅️ conversion ternaire → binaire
            self.beat1_candidates.append((start, start + 10, beat1, tempo))  # end = start + 10s (arbitraire)

        def update_menu():
            menu = self.beat1_selector["menu"]
            menu.delete(0, "end")
            for i, (start, end, beat1, tempo) in enumerate(self.beat1_candidates):
                label = f"{i+1}: {self.hms(start*1000)} → {self.hms(end*1000)} @ {int(tempo)} BPM"
                menu.add_command(label=label, command=lambda v=i: self.select_beat1_candidate(v))
            if self.beat1_candidates:
                first_start = self.beat1_candidates[0][0]
                label = f"✅ {1}: {self.hms(first_start * 1000)}"
                #self.beat1_selector_var.set(label)
                self.console.config(text=f"✅ {len(self.beat1_candidates)} count-ins détectés")
            else:
                self.beat1_selector_var.set("Aucun Beat 1")
                self.console.config(text="❌ Aucun count-in trouvé")

        self.root.after(0, update_menu)
    def select_beat1_candidate(self, index):
        if index >= len(self.beat1_candidates):
            self.console.config(text="❌ Index de beat1 invalide")
            return

        start, _, beat1, bpm = self.beat1_candidates[index]
        nb_measures = self.loop_length_var.get()

        duration = nb_measures * 60 / bpm * 4  # si 4 temps par mesure

        start_ms = int(start * 1000)
        duration_ms = int(duration * 1000)
        self.loop_start = start_ms
        self.loop_end = start_ms + duration_ms
        self.playhead = self.loop_start
        self.set_playhead_time(self.loop_start)

        # ✅ Affiche le choix dans le bouton
        label = f"🎯 {index + 1}: {self.hms(start_ms)}"
        self.beat1_selector_var.set(label)

        self.console.config(text=f"🎯 Loop A/B calée sur {nb_measures} mesures à {int(bpm)} BPM")
    def reset_force_playhead_time(self):
        self.force_playhead_time = False

    def set_playhead_time(self, milliseconds, force_jump=True):
        clamped_time_ms = max(0, min(milliseconds, self.duration - 100))
        self.last_jump_target_ms = clamped_time_ms

        # Brint(f"[TBD] ✯ set_playhead_time({clamped_time_ms}ms, force_jump={force_jump})")
        Brint(f"[TBD] ✯ set_playhead_time({self.hms(clamped_time_ms)}ms, force_jump={force_jump})")

        # Affiche une barre rose temporaire pendant 1s
        self.draw_temp_jump_marker(clamped_time_ms)

        if force_jump:
            # self.player.set_time(int(clamped_time_ms))
            self.safe_jump_to_time(int(clamped_time_ms), source="set_playhead_time")
            self.last_seek_time = time.time()

        self.console.config(text=f"✯ Position : {self.hms(int(clamped_time_ms))}")

    def draw_temp_jump_marker(self, ms):
        canvas = self.timeline
        canvas.delete("tempjump")
        t_sec = ms / 1000.0
        zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_end = zoom["zoom_end"]
        zoom_range = zoom["zoom_range"]

        if zoom_range <= 0:
            Brint(f"[ERROR] ❌ zoom_range invalide ({zoom_range}). Fallback full view.")
            zoom_start = 0
            zoom_end = self.duration / 1000.0
            zoom_range = zoom_end - zoom_start
            width = canvas.winfo_width()
            Brint("[ERROR] draw_temp_jump_marker: zoom_range = 0 ➔ annulation dessin")
            return
        width = canvas.winfo_width()

        x = self.time_sec_to_canvas_x(t_sec)
        canvas.create_line(x, 0, x, 24, fill="#f0a", width=2, dash=(4, 4), tags="tempjump")


    def jump(self, delta_sec):
        now = time.time() * 1000  # ms
        self.last_jump_timestamps.append(now)
        if len(self.last_jump_timestamps) > 3:
            self.last_jump_timestamps.pop(0)

        delta_ms = int(delta_sec * 1000)

        # ✅ Check d'abord si en mode édition A ou B
        mode = self.edit_mode.get()
        if mode == "loop_start" and self.loop_start is not None:
            self.loop_start = max(0, self.loop_start + delta_ms)
            
            
            # 🔄 Snap auto sur keyframe
            
            current_sec = self.loop_start / 1000.0
            if self.snap_to_keyframes_enabled:
                keyframes = self.extract_keyframes_around(self.current_path, current_sec, window_sec=2.0)
                snapped_sec = self.snap_to_closest_keyframe(current_sec, keyframes)
            else:
                snapped_sec = current_sec
            self.loop_start = int(snapped_sec * 1000)


            # 🔥 Test d'inversion après déplacement A
            if self.loop_end is not None and self.loop_start > self.loop_end:
                Brint("[TBD] ↔️ Inversion A/B après déplacement A")
                self.loop_start, self.loop_end = self.loop_end, self.loop_start
                self.console.config(text="↔️ Marqueurs inversés")

            self.set_playhead_time(self.loop_start, force_jump=False)
            # Brint("[TBD] jump to a NOWNOW")
            self.console.config(text=f"✏️ A déplacé à {self.hms(self.loop_start)}")
            return

        if mode == "loop_end" and self.loop_end is not None:
            self.loop_end = max(0, self.loop_end + delta_ms)

        # 🔄 Snap auto sur keyframe
            current_sec = self.loop_end / 1000.0
            if self.snap_to_keyframes_enabled:
                keyframes = self.extract_keyframes_around(self.current_path, current_sec, window_sec=2.0)
                snapped_sec = self.snap_to_closest_keyframe(current_sec, keyframes)
            else:
                snapped_sec = current_sec
            self.loop_end = int(snapped_sec * 1000)


            # 🔥 Test d'inversion après déplacement B
            if self.loop_start is not None and self.loop_start > self.loop_end:
                Brint("[TBD] ↔️ Inversion A/B après déplacement B")
                self.loop_start, self.loop_end = self.loop_end, self.loop_start
                self.console.config(text="↔️ Marqueurs inversés")

            self.set_playhead_time(self.loop_end, force_jump=False)
            self.console.config(text=f"✏️ B déplacé à {self.hms(self.loop_end)}")
            return

        # 🎯 Sinon comportement normal (playhead)
        if self.playhead_time is not None:
            current_ms = self.last_jump_target_ms
        else:
            current_ms = self.player.get_time()

        new_time = current_ms + delta_ms

        if self.loop_start and self.loop_end:
            new_time = max(self.loop_start, min(self.loop_end - 100, new_time))
        elif self.duration:
            new_time = max(0, min(self.duration - 100, new_time))

        # MAJ immédiate de la playhead visuelle
        self.last_jump_target_ms = new_time
        self.force_playhead_time = True  # ➔ Update immédiat du compteur et de la playhead
        # self.root.after(200, self.reset_force_playhead_time)


        # 🔥 Détection du spam (conserve ton système)
        if len(self.last_jump_timestamps) == 3:
            a, b, c = self.last_jump_timestamps
            if (b - a) < 100 and (c - b) < 100:
                self.spam_mode_active = True
                self.spam_mode_start_time = now
                self.force_playhead_time = True
                Brint("[TBD] 🚨 Spam détecté, cooldown activé")

                if self.player.is_playing():
                    self.player.pause()
                    Brint("[TBD] ⏸ VLC mis en pause à cause du spam")
        if self.spam_mode_active:
            Brint("[TBD] ⏳ En attente fin de spam cooldown (VLC pas encore mis à jour)")
            return  # VLC pas encore repositionné

        # 🎯 Si pas spam ➔ jump immédiat
        Brint(f"[TBD] 🎯 Jump immédiat vers {self.hms(new_time)}")
        # self.jump_to_time(new_time)
        self.safe_jump_to_time(new_time, source="Jump")
        self.needs_refresh = True
        self.refresh_static_timeline_elements()

    def record_loop_marker(self, mode, milliseconds=None, auto_exit=True):
        # 🛠️ Fallback logique si la boucle est inactive (A == B == 0)
        if self.loop_start == 0 and self.loop_end == 0:
            Brint("[RLM] ⚠️ Loop inactive, on fallback B = durée totale du média")
            self.loop_end = self.player.get_length()

        Brint(f"[RLM] STARTS➕ loop_start = {self.loop_start}, loop_end = {self.loop_end}")

        now = milliseconds if milliseconds is not None else self.player.get_time()
        # 🔐 Cas spécial : player.get_time() retourne 0 après un stop ➝ on récupère la vraie position de la playhead
        if mode == "loop_start" and now == 0 and milliseconds is None:
            if hasattr(self, "playhead_time") and self.playhead_time > 0:
                now = int(self.playhead_time * 1000)
                Brint(f"[RLM]✅ Correction de now depuis playhead_time → {now} ms")
            else:
                Brint("[RLM]❌ Ignoré : tentative de set A à 0 sans playhead valide")
                # 🖍️ Redessin de la playhead à la bonne position
                if hasattr(self, "playhead_time"):
                    # self.root.after(1000, lambda: self.update_playhead_by_time(self.playhead_time * 1000))
                    self.root.after(1000, lambda: self.safe_update_playhead(self.playhead_time * 1000, source="record_loop_marker"))

                return

        Brint(f"[RLM]🕹️ Enregistrement du marqueur {mode} @ {now} ms")

        temp_start = self.loop_start
        temp_end = self.loop_end
        inversion = False

        if mode == "loop_start":
            temp_start = now

            if self.snap_to_keyframes_enabled:
                keyframes = self.extract_keyframes_around(self.current_path, temp_start / 1000.0, window_sec=2.0)
                Brint(f"[RLM]🔎 Keyframes trouvées autour de A: {keyframes}")
                snapped = self.snap_to_closest_keyframe(temp_start / 1000.0, keyframes)
                temp_start = int(snapped * 1000)
            else:
                temp_start = int(temp_start)

            if self.loop_end is None and self.duration > 0:
                temp_end = self.duration - 1000
                Brint(f"[TBD] RLM]⚠️ B manquant – auto-fixé à {temp_end} ms")
                self.console.config(text="⚠️ B auto-fixé à la fin du fichier (-1s)")

        elif mode == "loop_end":
            temp_end = now

            if self.snap_to_keyframes_enabled:
                keyframes = self.extract_keyframes_around(self.current_path, temp_end / 1000.0, window_sec=2.0)
                Brint(f"[RLM]🔎 Keyframes trouvées autour de B: {keyframes}")
                snapped = self.snap_to_closest_keyframe(temp_end / 1000.0, keyframes)
                temp_end = int(snapped * 1000)
            else:
                temp_end = int(temp_end)

        Brint(f"[RLM]🔍 Avant inversion : A={temp_start} ms, B={temp_end} ms")

        # ↔️ Inversion automatique si A > B
        if temp_start is not None and temp_end is not None and temp_start > temp_end:
            temp_start, temp_end = temp_end, temp_start
            inversion = True
            Brint(f"[RLM]↔️ Inversion effectuée : A={temp_start}, B={temp_end}")
            self.console.config(text="↔️ Marqueurs A/B interchangés")

            # 🔁 Switch the active marker being edited
            new_mode = "loop_end" if mode == "loop_start" else "loop_start"
            if hasattr(self, "edit_mode"):
                self.edit_mode.set(new_mode)
            self.btn_edit_A.config(relief=tk.SUNKEN if new_mode == "loop_start" else tk.RAISED)
            self.btn_edit_B.config(relief=tk.SUNKEN if new_mode == "loop_end" else tk.RAISED)

            Brint(f"[RLM] Edit mode basculé en {new_mode} après inversion")

        # ✅ Affectation finale des marqueurs
        if mode == "loop_start" or inversion:
            self.loop_start = temp_start
        if mode == "loop_end" or inversion:
            self.loop_end = temp_end

        # Hits are kept in absolute time; do not shift when markers move


        Brint(f"[RLM]✅ Affectation finale : A={self.loop_start} | B={self.loop_end}")

        # If mode bar is enabled and we just set 'A', readjust 'B'
        if mode == "loop_start" and hasattr(self, 'mode_bar_enabled') and self.mode_bar_enabled:
            # Ensure one_bar_duration_ms is fresh based on current tempo when 'A' is set
            num_bars = getattr(self, 'mode_bar_bars', 1)
            if hasattr(self, 'tempo_bpm') and self.tempo_bpm and self.tempo_bpm > 0:
                self.one_bar_duration_ms = ((60000 / self.tempo_bpm) * 4) * num_bars
            else:
                self.one_bar_duration_ms = 4000 * num_bars # Default
            Brint(f"[RLM] Mode Bar ON (A set): Refreshed one_bar_duration_ms to {self.one_bar_duration_ms}ms for {num_bars} bar(s) using tempo {getattr(self, 'tempo_bpm', 'N/A')}.")

            if hasattr(self, 'adjust_b_marker_if_mode_bar_enabled'):
                Brint(f"[RLM] Mode bar is ON, A was set. Triggering B adjustment.")
                self.adjust_b_marker_if_mode_bar_enabled()
            else:
                Brint(f"[RLM] Mode bar is ON, A was set, but adjust_b_marker_if_mode_bar_enabled not found.")

        # 📏 Auto-zoom immédiat si les deux marqueurs viennent d’être définis
        if self.loop_start and self.loop_end:
            # self.auto_zoom_on_loop_markers(force=True)
            self.maybe_adjust_zoom_if_out_of_frame()



        if self.loop_start is not None and self.loop_end is not None:
            
            self.current_loop = LoopData(
                name=self.selected_loop_name or "Unnamed",
                loop_start=self.loop_start,
                loop_end=self.loop_end,
                key=self.current_loop.key if self.current_loop else "C",
                mode=self.current_loop.mode if self.current_loop else "ionian",
                chords=self.current_loop.chords if self.current_loop else [],
                master_note_list=self.current_loop.master_note_list if self.current_loop else [],
                tempo_bpm=self.current_loop.tempo_bpm if self.current_loop and self.current_loop.tempo_bpm else 60,
                loop_zoom_ratio = getattr(self.current_loop, "loop_zoom_ratio", 1.0)
            )

            Brint(f"[[RLM]] current_loop initialisée : {self.current_loop.name} | A={self.current_loop.loop_start} | B={self.current_loop.loop_end}")
            # 🧠 Zoom intelligent si les deux marqueurs viennent d'être posés pour la première fois
            if not hasattr(self, "_zoom_already_triggered") or not self._zoom_already_triggered:
                self._zoom_already_triggered = True
                self.auto_zoom_on_loop_markers(force=True)


        else:
            Brint("[[RLM]] Impossible d'initialiser current_loop car A ou B est invalide.")
            self.current_loop = None

        

        if auto_exit:
            must_jump = False
            if mode == "loop_end" and not inversion:
                must_jump = True
            if mode == "loop_start" and inversion:
                must_jump = True

            if must_jump:
                Brint("[RLM]🏁 Jump car nouveau A défini ou inversion")
                self.set_playhead_time(self.loop_start)

            self.clear_edit_mode()

        self.needs_refresh = True
        self.refresh_static_timeline_elements()
        Brint(f"[RLM] ENDS➕ loop_start = {self.loop_start}, loop_end = {self.loop_end}")
        self.invalidate_loop_name_if_modified()
        
        # self.GlobXa, self.GlobXb = self.get_loop_zoom_range()
        # ✅ Affectation finale : A=xxx | B=xxx
        Brint(f"[RLM]✅ Affectation finale : A={self.loop_start} | B={self.loop_end}")

        # 💡 Remise à jour forcée du loop_duration et du timestamp de saut
        if self.loop_start and self.loop_end:
            self.loop_duration_s = (self.loop_end - self.loop_start) / 1000.0
            self.last_loop_jump_time = time.perf_counter()
            Brint(f"[RLM]] Loop jump reset : loop_duration_s={self.loop_duration_s:.3f}s")
            
        self.maybe_adjust_zoom_if_out_of_frame()

        self.invalidate_jump_estimators()
        Brint("[RLM] ♻️ Cache precomputed_grid_infos invalidé à cause du déplacement de A ou B")
        self.precomputed_grid_infos = {}

        # Rebuild the rhythm grid to realign subdivisions with the new loop markers
        self.build_rhythm_grid()
        self.compute_rhythm_grid_infos()  # recompute using the fresh grid
        self.remap_persistent_validated_hits()
        if hasattr(self, "draw_rhythm_grid_canvas"):
            self.draw_rhythm_grid_canvas()

        # self.draw_loop_markers()
        self.refresh_static_timeline_elements()
        Brint("[RLM] 🖍️ Redessin forcé des marqueurs après zoom")




    def step_play(self):
        if not self.grid_times or self.player is None:
            Brint("[TBD] ⛔ Analyse non effectuée ou média non chargé.")
            return

        if self.step_mode_index >= len(self.grid_times):
            Brint("[TBD] 🔁 Fin de la grille atteinte. Reprise depuis 1.1.")
            self.step_mode_index = 0

        index = self.step_mode_index
        label = self.grid_labels[index]
        start = self.grid_times[index]
        duration_ms = int((60.0 / self.tempo) * 1000 / 3)
        # self.jump_to_time(int(start * 1000))  # ✅ important
        self.safe_jump_to_time(int(start * 1000), source="step_play")
        self.player.play()
        self.playhead_time = self.grid_times[self.step_mode_index]


        def pause_later():
            self.player.pause()
            self.label_subdivision.config(text=f"Subdivision: {label}")
            Brint(f"🎧 Lecture {index+1}/{len(self.grid_times)} @ {start:.3f}s [{label}]")
            self.step_mode_index += 1
            if self.autostep_enabled:
                self.root.after(duration_ms, self.step_play)

        self.root.after(duration_ms, pause_later)

    def step_back(self):
        if not self.grid_times or self.player is None:
            Brint("[TBD] ⛔ Analyse non effectuée ou média non chargé.")
            return

        self.step_mode_index = max(0, self.step_mode_index - 1)
        index = self.step_mode_index
        label = self.grid_labels[index]
        start = self.grid_times[index]
        duration_ms = int((60.0 / self.tempo) * 1000 / 3)
        # self.jump_to_time(int(start * 1000))  # ✅ important
        self.safe_jump_to_time(int(start * 1000), source="step_back")
        #self.jump_to_time(int(start))
        self.player.play()
        self.playhead_time = self.grid_times[self.step_mode_index]

        def pause_later():
            self.player.pause()
            self.label_subdivision.config(text=f"Subdivision: {label}")
            Brint(f"🔙 Lecture {index+1}/{len(self.grid_times)} @ {start:.3f}s [{label}]")

        self.root.after(duration_ms, pause_later)
    
    
    def get_musical_label(self, scientific_label):
        try:
            _, triolet, pos = map(int, scientific_label.split("."))
            return str(triolet) if pos == 1 else ["T", "L"][pos - 2]
        except:
            return scientific_label  # fallback


    def analyser_boucle(self):
        
        taille_buffer_ms = 100
        self.beat1_locked = True

        if not hasattr(self, 'media'):
            self.console.config(text="⚠️ Aucun fichier en lecture")
            return

        path = self.media.get_mrl().replace("file://", "").replace("%20", " ")
        if os.name == "nt" and path.startswith("/"):
            if dbflag : Brint("[DEBUG] Correction du chemin dans player.py")
            path = path[1:]

        loop_start_sec = self.loop_start / 1000 if self.loop_start else 0
        loop_end_sec = self.loop_end / 1000 if self.loop_end else (loop_start_sec + 10)

        Brint(f"[TBD] 🔍 Analyse boucle entre {loop_start_sec:.2f}s et {loop_end_sec:.2f}s")
        Brint(f"[TBD] 📁 Fichier : {path}")

        self.beat1 = loop_start_sec
        self.tempo = self.tempo_bpm

        # Brint(f"[TBD] ⏱ Beat1 déjà fixé : {self.beat1:.3f}")

        beat1 = self.beat1
        tempo = self.tempo
        self.set_tempo_bpm(tempo, source="analyzed")

        beat_interval = 60.0 / tempo
        triplet_offsets = [0.0, beat_interval / 3, 2 * beat_interval / 3]

        self.grid_times.clear()
        self.grid_labels.clear()
        for measure in range(1, 9):
            for triolet in range(1, 5):
                for pos in range(1, 3 + 1):
                    t = beat1 + (measure - 1) * 4 * beat_interval \
                            + (triolet - 1) * beat_interval \
                            + triplet_offsets[pos - 1]
                    self.grid_times.append(t)
                    self.grid_labels.append(f"{measure}.{triolet}.{pos}")

        loop_measures = self.loop_length_var.get()
        beats_per_measure = 4
        self.original_loop_end = loop_end_sec


        Brint(f"[TBD] 🔁 Snap Loop A = {loop_start_sec} | B = {loop_end_sec}")

        self.set_playhead_time(self.loop_start)
        self.step_mode_index = 0  # reset pour step_play
        start = time.time()
        
        duration = (loop_end_sec - loop_start_sec)  


        # Lancement de la prédiction sur le segment
        model_output, midi_data, note_events = predict_on_loop_segment(path, loop_start_sec, duration)

        # Sécurité : tri temporel explicite
        note_events = sorted(note_events, key=lambda note: note[0])  # note[0] = start_time

        # 🎯 Affichage de toutes les notes détectées dans l’intervalle A–B
        Brint(f"[TBD] 🎯 {len(note_events)} notes détectées dans l’intervalle A–B ({duration:.2f}s)")
        for note in note_events:
            try:
                start, end, pitch, conf = note[:4]
                pitch_name = pretty_midi.note_number_to_name(pitch)
                Brint(f"[TBD]  - {self.hms(start * 1000)} | Pitch: {pitch_name} | Confidence: {conf:.2f}")
            except Exception as e:
                Brint(f"[WARN] Erreur dans note: {note} => {e}")

        # 💾 Stockage dans la master liste des notes du loop (A–B)
        self.current_loop_master_notes = [
            [float(start), float(end), pretty_midi.note_number_to_name(pitch), float(conf)]
            for start, end, pitch, conf, *_ in note_events
            if loop_start_sec <= start < loop_end_sec
        ]

        Brint("[DEBUG] 🎼 Master notes filtrées et triées pour la boucle A–B :")
        for start, end, pitch, conf in self.current_loop_master_notes[:10]:  # affiche les 10 premières
            Brint(f"[TBD]  - {self.hms(start * 1000)} | Pitch: {pitch} | Confidence: {conf:.2f}")

        # self.threshold = getattr(self, 'threshold', 0.5)
        self.all_detected_notes = []
        for t in self.grid_times:
            group = [
                (pitch, conf)
                for start, end, pitch, conf in self.current_loop_master_notes
                if abs(start - t) < 0.09
            ]
            self.all_detected_notes.append(group)


        total_steps = len(self.grid_labels)
        total_bars = (len(self.grid_labels) + 11) // 12
        if not hasattr(self, "chord_sequence") or len(self.chord_sequence) < total_bars:
            self.chord_sequence = [("F7", "F"), ("Bb7", "Bb")] * total_bars
            Brint(f"[DEBUG] chord_sequence initialisée avec {len(self.chord_sequence)} mesures")
        self.result_box.config(state='normal')
        self.result_box.delete('1.0', tk.END)
        
        self.result_box.insert(tk.END, "🎼 Analyse RHYTHMique :\nTemps\tTimestamp\tNote\tAccord\tDegré\n")
        self.refresh_note_display()
        pass#self.result_box.config(state='disabled')



    def set_edit_mode(self, mode):
        current = self.edit_mode.get()
        if current == mode:
            # ✅ Si on reclique sur le bouton actif → repasser en mode playhead
            self.edit_mode.set("playhead")
            self.console.config(text="🎯 Mode : Playhead")
            Brint(f"[EDIT MODE] Quitte le mode {mode.upper()}, retour en mode playhead")
        else:
            self.edit_mode.set(mode)
            label = "A" if mode == "loop_start" else "B" if mode == "loop_end" else "Playhead"
            self.console.config(text=f"✏️ Mode édition : {label}")
            Brint(f"[EDIT MODE] Active le mode {label}")

        # Ensure key bindings remain responsive when toggling edit mode
        self.root.focus_set()

        # 🔄 Met à jour l’état visuel des boutons
        self.btn_edit_A.config(relief=tk.SUNKEN if self.edit_mode.get() == "loop_start" else tk.RAISED)
        self.btn_edit_B.config(relief=tk.SUNKEN if self.edit_mode.get() == "loop_end" else tk.RAISED)
    def clear_loop(self, _=None):
        Brint("[CLEAR]Clear Loop")
        self.raw_hit_memory.clear()

        self.cached_canvas_width = self.grid_canvas.winfo_width()
        if hasattr(self, "current_loop") and getattr(self, "current_loop", None):
            if hasattr(self.current_loop, "chords"):
                self.current_loop.chords = []
                self.current_loop.mapped_notes = {}
                Brint("[CLEAR LOOP] 🎵 Accords de la boucle supprimés")


        # Ensure zoom shows the entire file when clearing the loop
        if hasattr(self, "zoom_ratio_var"):
            self.zoom_ratio_var.set(1.0)
        self.apply_loop_zoom_ratio(1.0)

        if hasattr(self, "player"):
            self.player.audio_set_mute(False)

        # 🔍 Durée via player.get_length()
        full_duration = self.player.get_length() if hasattr(self, "player") else 0
        Brint(f"[CLEAR LOOP] Durée vidéo détectée : {full_duration} ms")
        if not full_duration or full_duration <= 0:
            Brint("[CLEAR LOOP WARNING] Durée invalide, fallback 1000 ms")
            full_duration = 1000

        # Reset loop markers to cover full media
        self.loop_start = 0
        self.loop_end = full_duration

        # Reset loop related state to avoid stale interpolation behaviour
        self.loop_pass_count = 0
        self.loop_duration_s = None
        self.awaiting_vlc_jump = False
        self.freeze_interpolation = False

        self.edit_mode.set("playhead")
        if hasattr(self, "btn_edit_A"):
            self.btn_edit_A.config(relief="raised")
        if hasattr(self, "btn_edit_B"):
            self.btn_edit_B.config(relief="raised")

        if hasattr(self, "current_loop") and getattr(self, "current_loop", None):
            self.current_loop.loop_start = 0
            self.current_loop.loop_end = full_duration

        if not hasattr(self, "zoom_context"):
            self.zoom_context = {}

        self.zoom_context["zoom_start"] = 0
        self.zoom_context["zoom_end"] = full_duration
        self.zoom_context["zoom_range"] = full_duration

        
        # Force Tkinter à mettre à jour les dimensions avant de dessiner
        self.timeline.delete("loop_marker")
        self.grid_canvas.delete("overlay_harmony")  # si tu tags tes overlays harmoniques
        self.grid_canvas.delete("rhythm_grid")      # si tu tags la grille RHYTHMique

        self.reset_rhythm_overlay()
        self.root.update_idletasks()

        self.safe_update_playhead(self.loop_start, source="clear_loop (reset playhead)")
        self.needs_refresh = True
        self.refresh_static_timeline_elements()
        self.draw_harmony_grid_overlay()

        self.update_loop()

        
    def toggle_pause(self, event=None):
        if not hasattr(self, "is_paused"):
            self.is_paused = False

        if not self.is_paused:
            # --- PAUSE ---
            self.is_paused = True
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            vlc_time = self.player.get_time()
            self.playhead_time = vlc_time / 1000.0
            self.pause_start_time = time.perf_counter()
            self.player.pause()
            self.console.config(text="⏸ Pause")
            Brint(f"[PH PAUSE] ⏸ Pause → VLC time = {vlc_time} ms → playhead_time = {self.playhead_time:.3f}s")

        else:
            # --- RESUME ---
            self.is_paused = False
            if self.playhead_time is not None:
                Brint(f"[PH PAUSE] ▶️ Reprise → saut à playhead_time = {self.playhead_time:.3f}s")
                self.safe_jump_to_time(int(self.playhead_time * 1000), source="toggle_pause")
            else:
                Brint("[PH PAUSE] ❓ Reprise → playhead_time manquant")
            if hasattr(self, "pause_start_time") and self.pause_start_time is not None:
                pause_duration = time.perf_counter() - self.pause_start_time
                if hasattr(self, "last_loop_jump_time"):
                    self.last_loop_jump_time += pause_duration
                self.pause_start_time = None
            self.player.play()
            self.console.config(text="▶️ Lecture")
            self.update_loop()

 
 
    def open_file(self, spawn_new_instance=False):
        if getattr(self, "after_id", None):
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.needs_refresh = True
        self.refresh_static_timeline_elements()

        path = filedialog.askopenfilename()
        if not path:
            return
        if spawn_new_instance:
            import subprocess
            import sys
            subprocess.Popen([sys.executable, os.path.abspath(__file__), path])
            self.root.destroy()
            sys.exit(0)
            return
        self.current_path = path
        self.root.after(1000, self.load_screen_zoom_prefs)

        import subprocess
        import tempfile
        import shutil

        def faststart_remux(input_path):
            temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            try:
                cmd = [
                    "ffmpeg", "-y",
                    "-i", input_path,
                    "-c", "copy",
                    "-movflags", "+faststart",
                    temp_output
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                shutil.move(temp_output, input_path)
                Brint(f"[TBD] ✅ Remux faststart appliqué sur {input_path}")
            except Exception as e:
                Brint(f"[TBD] ⚠️ Remux échoué : {e}")
            finally:
                if os.path.exists(temp_output) and temp_output != input_path: # Ensure we don't delete the original if move failed
                    os.remove(temp_output)
                    Brint(f"[TEMP CLEANUP] Removed temporary remux file: {temp_output}")


        # Lance automatiquement le remux
        # faststart_remux(self.current_path)

        self.media = self.instance.media_new(path)
        self.load_saved_loops()
        # self.keyframes = self.extract_keyframes(path)

        self.player.set_media(self.media)
        self.player.set_hwnd(self.canvas.winfo_id())
        self.audio_power_data = None
        self.audio_power_max = 0.0
        import threading as _thread
        _thread.Thread(target=self._compute_audio_power_data, daemon=True).start()
        # self.apply_crop()  # <-- Recharge le zoom enregistré

        self.playhead_time = 0.0
        self.last_jump_target_ms = 0
        self.safe_update_playhead(0, source="faststart_remux")

        self.player.play()
        # self.root.after(1000, self.reset_force_playhead_time)

        if hasattr(self, "player"):
            self.player.audio_set_mute(False)

        if dbflag : pass #Brint(f"[DEBUG] open_file(): get_length() = {self.player.get_length()} ms")

        self.safe_update_playhead(0, source="faststart_remux2")  # 👈 Affiche playhead immédiatement
        self.root.after(100, self.update_loop)
        self.console.config(text=f"▶️ Playing: {os.path.basename(path)}")
        import threading
    # threading.Thread(target=self.load_jamtrack_zones, args=(self.current_path,), daemon=True).start()
        threading.Thread(target=self._run_beat1_detection_from_scanfile, daemon=True).start()

        if dbflag : pass #Brint(f"[DEBUG] open_file(): tentative de get_length() = {self.player.get_length()} ms")
        self.add_recent_file(self.current_path)
        self.apply_crop() 

    def update_loop(self):
        self.root.bind('t', lambda e: self.tap_tempo())
        self.update_state_window()

        if self.grid_visible:
            self.draw_rhythm_grid_canvas()

        if self.player.get_media():
            dur = self.player.get_length()
            is_playing = self.player.is_playing()
            player_rate = self.player.get_rate()
            if player_rate <= 0:
                player_rate = 1.0

            player_now = self.player.get_time()
            self.duration = dur

            if self.loop_start and self.loop_end:
                if not hasattr(self, 'last_loop_jump_time'):
                    self.last_loop_jump_time = time.perf_counter()

                # Ensure loop_duration_s is defined whenever we have valid loop markers
                if self.loop_duration_s is None or self.loop_duration_s <= 0:
                    self.loop_duration_s = (self.loop_end - self.loop_start) / 1000.0
                    Brint(f"[INIT LOOP] loop_duration_s = {self.loop_duration_s:.3f}s")

                # Resume interpolation once VLC confirms it is playing from A
                if self.awaiting_vlc_jump and is_playing:
                    if abs(player_now - self.loop_start) < 20:
                        self.awaiting_vlc_jump = False
                        self.freeze_interpolation = False
                        self.last_loop_jump_time = time.perf_counter()
                        Brint("[LOOP RESYNC] Interpolation resumed after jump")

                if self.interp_var.get() and not self.freeze_interpolation:
                    elapsed_since_last_jump = time.perf_counter() - self.last_loop_jump_time
                    loop_duration_corrected = self.loop_duration_s / player_rate
                    wrapped_elapsed = elapsed_since_last_jump % loop_duration_corrected
                    interpolated = self.loop_start / 1000.0 + wrapped_elapsed * player_rate
                    Brint(f"[PH LOOP] 🎯 Interpolation = {interpolated:.3f}s (elapsed={elapsed_since_last_jump:.3f}s)")
                    self.safe_update_playhead(interpolated * 1000, source="Loop interpolation")

                    if elapsed_since_last_jump >= loop_duration_corrected:
                        self.safe_jump_to_time(self.loop_start, source="Jump B estim (all rates)")
                        self.last_loop_jump_time = time.perf_counter()
                        self.freeze_interpolation = True
                        self.awaiting_vlc_jump = True
                        self.loop_pass_count += 1
                        Brint(f"[LOOP PASS] Boucle AB passée {self.loop_pass_count} fois")
                        self.decay_subdivision_states()
                        self.associate_hits_to_subdivisions()
                        self.update_subdivision_states()
                        self.last_playhead_time = self.playhead_time
                        for i in list(self.subdivision_counters.keys()):
                            last_hit_loop = self.subdiv_last_hit_loop.get(i, -1)
                            if 0 < self.subdivision_counters[i] < 3:
                                if last_hit_loop <= self.loop_pass_count - 2:
                                    Brint(f"[DECAY] Subdiv {i} remise à zéro (dernier hit = loop {last_hit_loop}, loop courante = {self.loop_pass_count})")
                                    self.subdivision_counters[i] = 0
                                    if i in self.subdiv_last_hit_loop:
                                        del self.subdiv_last_hit_loop[i]
                else:
                    self.safe_update_playhead(player_now, source="VLC loop raw")
                    if player_now >= self.loop_end:
                        self.safe_jump_to_time(self.loop_start, source="Jump B raw")
                        self.last_loop_jump_time = time.perf_counter()
                        self.loop_pass_count += 1
                        Brint(f"[LOOP PASS] Boucle AB passée {self.loop_pass_count} fois (raw)")
                        self.decay_subdivision_states()
                        self.associate_hits_to_subdivisions()
                        self.update_subdivision_states()
                        self.last_playhead_time = self.playhead_time
                        for i in list(self.subdivision_counters.keys()):
                            last_hit_loop = self.subdiv_last_hit_loop.get(i, -1)
                            if 0 < self.subdivision_counters[i] < 3:
                                if last_hit_loop <= self.loop_pass_count - 2:
                                    Brint(f"[DECAY] Subdiv {i} remise à zéro (dernier hit = loop {last_hit_loop}, loop courante = {self.loop_pass_count})")
                                    self.subdivision_counters[i] = 0
                                    if i in self.subdiv_last_hit_loop:
                                        del self.subdiv_last_hit_loop[i]
            else:
                self.safe_update_playhead(player_now, source="VLC raw mode")
                # dans le cas classique (pas de boucle)
                Brint(f"[PH VLC] 🎯 Position brute VLC = {player_now} ms → set")

            self.time_display.config(text=f"⏱ {self.hms(self.playhead_time * 1000)} / {self.hms(self.duration)}")

        if self.spam_mode_active:
            Brint("[TBD]  spam")
            now = time.time() * 1000
            

            if now - self.spam_mode_start_time > self.spam_cooldown_ms:
                Brint("[TBD] ✅ Cooldown terminé, retour à l'état normal")
                self.spam_mode_active = False
                self.last_jump_timestamps.clear()

                if self.last_jump_target_ms is not None:
                    Brint(f"[PH SPAM] 🎯 Cooldown → recalage sur {self.last_jump_target_ms} ms")
                    self.safe_jump_to_time(int(self.last_jump_target_ms), source="update_loop")
                    # dans le spam cooldown

#fps
        if self.pause_each_update.get():
            self.is_paused = True
        if not self.is_paused:
            try:
                delay = int(self.update_delay_ms_var.get())
                if delay < 1:
                    delay = 1
            except Exception:
                delay = 30
                self.update_delay_ms_var.set(delay)
            self.after_id = self.root.after(delay, self.update_loop)


    def on_timeline_click(self, e): self.handle_timeline_interaction(e.x)
    def on_timeline_drag(self, e): self.handle_timeline_interaction(e.x)
    def handle_timeline_interaction(self, x):
        if self.duration <= 0:
            return

        if self.cached_width is None or time.time() - self.last_width_update > 1:
            self.cached_width = self.timeline.winfo_width()
            self.last_width_update = time.time()
        width = self.cached_width

        zoom = self.get_zoom_context()
        zoom_start_ms = zoom["zoom_start"]
        zoom_end_ms = zoom["zoom_end"]
        zoom_range_ms = zoom["zoom_range"]

        if zoom_range_ms <= 0:
            Brint(f"[ERROR] ❌ zoom_range invalide ({zoom_range_ms} ms). Fallback full view.")
            zoom_start_ms = 0
            zoom_end_ms = self.duration
            zoom_range_ms = zoom_end_ms - zoom_start_ms

        # Convertir en secondes juste pour t_sec
        t_ms = zoom_start_ms + int((x / width) * zoom_range_ms)
        t_sec = t_ms / 1000.0
        mode = self.edit_mode.get()
        Brint(f"[CLICK] Timeline click @ {t_ms}ms | Mode = {mode}")

        # 🛑 Si clic timeline → priorité utilisateur : stoppe spam-mode
        self.spam_mode_active = False
        self.force_playhead_time = False
        self.force_playhead_time_until = 0
        self.last_jump_timestamps.clear()
        Brint("[TBD] 🖱️ Clic timeline : spam-mode annulé")

        if mode == "loop_start":
            self.record_loop_marker("loop_start", t_ms, auto_exit=False)
        elif mode == "loop_end":
            self.record_loop_marker("loop_end", t_ms, auto_exit=False)
        else:
            self.set_playhead_time(t_ms, force_jump=True)

    def record_loop_marker_from_timeline(self, milliseconds):
        """Méthode appelée quand on clique sur la timeline en mode édition A ou B."""
        if self.edit_mode not in ("loop_start", "loop_end"):
            Brint("[TBD] ⚠️ Pas en mode édition A ou B — clic ignoré.")
            return

        Brint(f"[TBD] 🖱️ Timeline set {self.edit_mode} @ {milliseconds} ms")

        # On appelle record_loop_marker avec la bonne intention
        self.record_loop_marker(self.edit_mode, milliseconds, auto_exit=False)



    def save_ab_to_mp3(self, repeat=False):
        Brint(f"[TBD] repeat{repeat}")
        if not self.loop_start or not self.loop_end:
            self.console.config(text="⚠️ Marqueurs A et B non définis")
            return

        input_path = self.current_path
        if not os.path.exists(input_path):
            self.console.config(text="❌ Fichier source introuvable")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("Fichiers MP3", "*.mp3")],
            title="Sauvegarder la boucle A-B"
        )
        if not output_path:
            return

        start_sec = self.loop_start / 1000.0
        duration_sec = (self.loop_end - self.loop_start) / 1000.0

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-i", input_path,
        ]

        if repeat:
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_sec),
                "-t", str(duration_sec),
                "-i", input_path,
                "-stream_loop", "9",  # 9 répétitions = 10 au total
                "-acodec", "libmp3lame",
                "-b:a", "192k",
                output_path
            ]
        else:
            cmd += ["-acodec", "libmp3lame", "-b:a", "192k", output_path]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.console.config(text=f"✅ Boucle exportée : {os.path.basename(output_path)}")




    def draw_rhythm_grid_canvas(self):
        Brint("[RHYTHM GRID] ➡ Démarrage draw_rhythm_grid_canvas()")  # 💡 AJOUT DEBUG SYSTEMATIQUE
        if not getattr(self, "rhythm_grid_enabled", True):
            if self.grid_canvas:
                self.grid_canvas.delete("rhythm_grid")
                self.grid_canvas.delete("syllabic_label")
                self.grid_canvas.delete("syllabic_hit")
                self.grid_canvas.delete("heatmap_filtered")
            Brint("[RHYTHM GRID] ⛔ Hidden")
            return
        if not self.is_loop_effectively_defined():
            Brint("[RHYTHM GRID] ❌ Loop incomplète (A=0 ou B=duration) → grille non affichée")
            return

        if not self.grid_subdivs:
            Brint("[RHYTHM ERROR] ❌ draw_rhythm_grid_canvas() appelé sans grid_subdivs valides")
        else:
            Brint(f"[DEBUG RHYTHM GRID SUBDIVS from draw_rhythm_grid_canvas] ▶️ Affichage des {min(len(self.grid_subdivs), 3)} premières subdivisions :")
            for i, (idx, t) in enumerate(self.grid_subdivs[:3]):
                x = self.time_sec_to_canvas_x(t)
                Brint(f"[RHYTHM GRID]  Subdiv {idx}: t={t:.3f}s ({int(t*1000)}ms) → x={x}px )")

        
        if self.loop_start is None or self.loop_end is None:
            Brint("[RHYTHM GRID] Loop A–B non définie. Skip draw_rhythm_grid_canvas().")
            return


        if not self.grid_canvas or self.loop_start is None or self.tempo_bpm is None:
            Brint("[RHYTHM GRID] ❌ Conditions non remplies : canvas ou tempo manquant.")  # 💡 MODIF
            return
        zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_end = zoom["zoom_end"]
        zoom_range = zoom["zoom_range"]

        if (zoom_range) <= 0:
            Brint("[RHYTHM GRID] ❌ GlobXb - GlobXa <= 0 : impossible de dessiner")
            return

        # ❗ On NE supprime PAS les éléments impact_vfx ici
        self.grid_canvas.delete("rhythm_grid")
        self.grid_canvas.delete("syllabic_label")
        self.grid_canvas.delete("syllabic_hit")
        self.grid_canvas.delete("harmony_grid")

        # self.grid_canvas.delete('all')
        self.grid_lines = []
        canvas_width = self.grid_canvas.winfo_width()

        Brint(f"[RHYTHM GRID] 📏 canvas_width = {canvas_width}")
        if canvas_width <= 10:
            Brint("[RHYTHM GRID] ⏳ Canvas trop petit, retry dans 100ms")
            self.grid_canvas.after(100, self.draw_rhythm_grid_canvas)
            return

        # Intervalle en secondes entre deux temps
        interval_sec = 60.0 / self.tempo_bpm
        Brint(f"[RHYTHM GRID] 🕒 Intervalle entre beats = {interval_sec:.3f}s")


        beats_per_measure=4


        # Espacement visuel (pixels par beat)
        loop_duration_sec = (self.loop_end - self.loop_start) / 1000.0

        if loop_duration_sec <= 0 or interval_sec <= 0:
            Brint("[RHYTHM GRID] ❌ Impossible de calculer pixels_per_beat")
            return

        if not self.debug_show_beat_lines_only:
            zoom = self.get_zoom_context()
            zoom_start = zoom["zoom_start"]
            zoom_end = zoom["zoom_end"]
            zoom_range = zoom["zoom_range"]

            canvas_height = self.grid_canvas.winfo_height()

            
            dynamic_factor = 0.90 if zoom_range < (self.loop_end - self.loop_start) else 1.0
            pixels_per_beat = 1000 * interval_sec * canvas_width * dynamic_factor / zoom_range

            # x_beat1 = time_to_x(self.loop_start / 1000.0)
            x_beat1 = self.time_sec_to_canvas_x(self.loop_start / 1000.0)

            max_beats_left = int(x_beat1 // pixels_per_beat) + 1
            max_beats_right = int((canvas_width - x_beat1) // pixels_per_beat) + 1

            subdivisions_per_beat = self.get_subdivisions_per_beat()


            pixels_per_subdiv = pixels_per_beat / subdivisions_per_beat
            mode = self.subdivision_mode
            Brint(f"[RHYTHM GRID] 🔍 playhead_canvas_x = {getattr(self, 'playhead_canvas_x', '❌ Not Set')}")


            for i in range(-max_beats_left * subdivisions_per_beat,
                           max_beats_right * subdivisions_per_beat + 1):
                x = x_beat1 + i * pixels_per_subdiv
                if 0 <= x <= canvas_width:
                    is_main_beat = (i % subdivisions_per_beat == 0)

                    bounce_x = getattr(self, "_grid_bounce_x", -9999)
                    bounce_ts = getattr(self, "_grid_bounce_ts", None)

                    if bounce_x is None:
                        bounce_x = -9999
                    if bounce_ts is None:
                        bounce_ts = 0

                    highlighted = abs(x - getattr(self, 'playhead_canvas_x', -9999)) < (pixels_per_subdiv / 2)

                    if is_main_beat:
                        beat_index = i // subdivisions_per_beat
                        beat_in_measure = beat_index % beats_per_measure
                        color = {
                            0: "blue",
                            2: "purple",
                            1: "#FFC107", #yellow
                            3: "#FFC107", #yellow
                        }.get(beat_in_measure, "gray")
                        width = 4 if highlighted else 2

                    elif (mode == "binary16" and i % 4 == 2) or (mode == "ternary16" and i % 6 == 3):
                        color = "gray"
                        width = 4 if highlighted else 2

                    else:
                        color = "lightgray"
                        width = 4 if highlighted else 1

                    self.grid_canvas.create_line(x, 0, x, canvas_height, fill=color, width=width , tags=("rhythm_grid",))
                    self.grid_lines.append((x, is_main_beat))
                    # ➡ On réinitialise proprement la heatmap en se basant sur la grille existante


         # 💡 AJOUT SYSTEMATIQUE POUR DEBUG ET RESET
            Brint("[RHYTHM GRID] ➡ build_rhythm_grid()")
            self.build_rhythm_grid()
            
            if not hasattr(self, "grid_subdivs") or not self.grid_subdivs:
                Brint("[RHYTHM GRID ERROR] ❌ draw_rhythm_grid_canvas() appelé sans grid_subdivs valides")
            else:
                Brint(f"[DEBUG RHYTHM GRID SUBDIVS from draw_rhythm_grid_canvas] ▶️ Affichage des {min(len(self.grid_subdivs), 3)} premières subdivisions :")
                for i, (idx, t) in enumerate(self.grid_subdivs[:3]):
                    x = self.time_sec_to_canvas_x(t)
                    pass#Brint(f"[TBD]   Subdiv {idx}: t={t:.3f}s ({int(t*1000)}ms) → x={x}px )")

            if self.grid_subdivs:
                Brint("[DEBUG RHYTHM GRID SUBDIVS from draw_rhythm_grid_canvas] ▶️ Affichage des 3 premières subdivisions :")
                for i, (idx, t_sec) in enumerate(self.grid_subdivs[:3]):
                    t_ms = t_sec * 1000
                    x = self.time_sec_to_canvas_x(t_sec)
                    Brint(f"[RHYTHM GRID]  Subdiv {idx}: t={t_sec:.3f}s ({int(t_ms)}ms) → x={x}px )")
            else:
                Brint("[DEBUG RHYTHM GRID SUBDIVS from draw_rhythm_grid_canvas ] ❌ Aucune subdivision générée.")

            Brint(f"[RHYTHM GRID] ✅ grid_subdivs initialisé : {len(self.grid_subdivs)} subdivisions.")  # 💡 AJOUT DEBUG

            # 💡 AJOUT ICI : Calcul systématique du pool unique
            # Brint("[RHYTHM GRID] ➡ Calcul precomputed_grid_infos")
            self.compute_rhythm_grid_infos()  # 💡 AJOUT FORTEMENT RECOMMANDÉ ICI

            # 💡 ENSUITE SEULEMENT les appels à heatmap
            Brint("[RHYTHM GRID] ➡ Appel draw_syllabic_grid_heatmap()")
            self.draw_syllabic_grid_heatmap()
            self.draw_harmony_grid_overlay()
            Brint("[RHYTHM GRID] ✅ Fin draw_rhythm_grid_canvas()")  # 💡 AJOUT DEBUG FINAL
       
    def on_user_hit(self, event=None):
        current_time_ms = self.playhead_time * 1000
        current_time_sec = self.playhead_time  # déjà en secondes
        
        # Phase 1 : ligne visible avec "bounce"
        x = getattr(self, 'playhead_canvas_x', None) # Restored original line

        if x is None or not isinstance(x, (int, float)) or x < 0:
            Brint(f"[HIT FX] ❌ x playhead_canvas_x ({x}) is invalid — impact visuel annulé")
            # Fallback or decide not to draw the visual effect if x is invalid
        else:
            canvas = self.grid_canvas
            canvas_height = canvas.winfo_height()

            line_id = canvas.create_line(
                x, 0, x, canvas_height,
                fill="#FF66CC",
                width=2,
                tags=("impact_vfx",)
            )
            Brint(f"[HIT FX] 💥 Impact visuel créé à x={x:.1f}px (line_id={line_id})")

            # Bounce rapide (using new try_itemconfig helper)
            canvas.after(50, lambda lid=line_id: self.try_itemconfig(canvas, lid, width=6))
            canvas.after(200, lambda lid=line_id: self.try_itemconfig(canvas, lid, width=4))
            canvas.after(400, lambda lid=line_id: self.try_itemconfig(canvas, lid, width=3))
            canvas.after(800, lambda lid=line_id: self.try_itemconfig(canvas, lid, width=1))

            # 💨 Ajout effet de disparition (transparence simulée)
            canvas.after(1000, lambda lid=line_id: self.try_itemconfig(canvas, lid, fill="#FFBBDD"))
            canvas.after(1200, lambda lid=line_id: self._remove_impact_vfx(lid)) # _remove_impact_vfx now handles try-except
        
        Brint(f"[HIT] 🎯 Fonction on_user_hit() appelée")
        Brint(f"[HIT] Frappe utilisateur à {self.hms(current_time_ms)} hms")

        self.record_user_hit(int(current_time_ms))

        precomputed = self.precomputed_grid_infos or self.compute_rhythm_grid_infos()
        self.precomputed_grid_infos = precomputed

        # 1. Calcul de l'espacement moyen entre subdivisions
        grid_times = [info['t_subdiv_sec'] for info in self.precomputed_grid_infos.values()]
        grid_times = sorted(grid_times)
        intervals = [t2 - t1 for t1, t2 in zip(grid_times[:-1], grid_times[1:])]
        avg_interval_sec = sum(intervals) / len(intervals) if intervals else 0.5  # fallback = 0.5s
        # Wider tolerance so hits always find a subdivision
        tolerance = avg_interval_sec / 2.0

        Brint(f"[HIT WINDOW] ⏱ Dynamic tolerance = {tolerance:.3f}s (1/2 of {avg_interval_sec:.3f}s)")

        # 2. Étendre temporairement les subdivisions pour la détection (±2 subdivs)
    
        

        
       
                
    def draw_syllabic_grid_heatmap(self):
        precomputed = self.precomputed_grid_infos or self.compute_rhythm_grid_infos()
        Brint("[DRAW HIT] Utilisation du cache precomputed_grid_infos")

        canvas = self.grid_canvas
        canvas_height = canvas.winfo_height()

        dynamic_hits = self.match_hits_to_subdivs()

        for i, subdiv_info in precomputed.items():
            x = subdiv_info['x']
            label = subdiv_info['label']
            state = subdiv_info['state']
            is_playhead = subdiv_info['is_playhead']
            user_hits = dynamic_hits.get(i, 0)

            if i < 3:
                Brint(f"[HIT draw_syllabic_grid_heatmap] Subdiv {i} | X={x:.1f}px | Label={label} | State={state} | Hits={user_hits}")

            if x < 0 or x > canvas.winfo_width():
                continue

            # Color and font size depend on subdivision state
            color = (
                "#FF0000" if state == 3 else
                "#DAA520" if state == 2 else
                "#555555" if state == 1 else
                "#00FF00" if is_playhead else
                "#CCCCCC"
            )
            font_size = (
                16 if state == 3 else
                14 if state == 2 else
                12 if state == 1 else
                14 if is_playhead else
                10
            )

            canvas.create_text(x, canvas_height / 2,
                               text=label,
                               fill=color,
                               font=("Arial", font_size, "bold"),
                               tags=("syllabic_label",))

            if user_hits > 0:
                canvas.create_oval(x - 10, canvas_height / 2 - 10, x + 10, canvas_height / 2 + 10,
                                   outline=color, width=2, tags=("syllabic_hit",))
                Brint(f"[DRAW HIT] ✅ cercle hit sur Subdiv {i} (x={x:.1f}px)")
    # def draw_syllabic_grid_heatmap(self):
        # precomputed = self.precomputed_grid_infos or self.compute_rhythm_grid_infos()
        # Brint("[DRAW HIT] Utilisation du cache precomputed_grid_infos")

        # canvas = self.grid_canvas
        # canvas_height = canvas.winfo_height()

        # # 🔄 Supprimer les anciens labels/hits avant redraw
        # canvas.delete("syllabic_label")
        # canvas.delete("syllabic_hit")

        # dynamic_hits = self.match_hits_to_subdivs()

        # for i, subdiv_info in precomputed.items():
            # x = subdiv_info['x']
            # label = subdiv_info['label']
            # state = subdiv_info['state']
            # is_playhead = subdiv_info['is_playhead']
            # user_hits = dynamic_hits.get(i, 0)

            # if x < 0 or x > canvas.winfo_width():
                # continue

            # if i < 3:
                # Brint(f"[HIT draw_syllabic_grid_heatmap] Subdiv {i} | X={x:.1f}px | Label={label} | State={state} | Hits={user_hits}")

            # # 🎨 Couleurs en fonction du state
            # if state == 3:
                # color = "#FF0000"  # rouge validé
                # font_size = 16
            # elif state == 2:
                # color = "#DAA520"  # orange (2e hit)
                # font_size = 14
            # elif state == 1:
                # color = "#555555"  # gris foncé (1er hit)
                # font_size = 12
            # elif is_playhead:
                # color = "#00FF00"  # vert fluo
                # font_size = 14
            # else:
                # color = "#CCCCCC"  # gris clair neutre
                # font_size = 10

            # # 🏷️ Affichage du label
            # canvas.create_text(
                # x, canvas_height / 2,
                # text=label,
                # fill=color,
                # font=("Arial", font_size, "bold"),
                # tags=("syllabic_label",)
            # )

            # # 🟠 Cercle de hit (optionnel selon `user_hits`)
            # if user_hits > 0:
                # canvas.create_oval(
                    # x - 10, canvas_height / 2 - 10,
                    # x + 10, canvas_height / 2 + 10,
                    # outline=color,
                    # width=2,
                    # tags=("syllabic_hit",)
                # )
                # Brint(f"[DRAW HIT] ✅ cercle hit sur Subdiv {i} (x={x:.1f}px)")




    def draw_filtered_rhythmic_heatmap(self):
        if not hasattr(self, "subdivision_counters") or not self.grid_times:
            return

        total_hits = sum(self.subdivision_counters.values())
        if total_hits == 0:
            return

        canvas = self.grid_canvas
        canvas_height = self.grid_canvas.winfo_height()

        for i, t_subdiv_sec in enumerate(self.grid_times):
            count = self.subdivision_counters.get(i, 0)
            if count == 0:
                continue  # On ne dessine que si frappes

            x_pos = self.time_sec_to_canvas_x(t_subdiv_sec)
            label = self.grid_labels[i] if i < len(self.grid_labels) else "?"
            color = "#FF0000" if count > 3 else "#FF8800"
            width = 4 + count * 2

            canvas.create_line(x_pos, 0, x_pos, canvas_height, fill=color, width=width, tags=("heatmap_filtered",))
            if i<3 : Brint(f"[HIT FILTERED] Subdiv {i:03d} | x={x_pos:.1f}px | Count={count} | Label={label} | Width={width}")

            canvas.create_text(x_pos, canvas_height / 2, text=label, fill=color, anchor="center", font=("Arial", 12, "bold"), tags=("heatmap_filtered",))


    def draw_harmony_grid_overlay(self):
        if not getattr(self, "harmony_grid_enabled", True):
            if self.harmony_canvas:
                self.harmony_canvas.delete("all")
            Brint("[HARMONY] ⛔ Hidden")
            return

        if self.is_loop_fully_cleared():
            self.harmony_canvas.delete("all")  # ou ".delete('overlay_harmony')" si tu as taggé
            # 🧽 Réinitialisation des labels pour éviter qu’ils soient redessinés
            if hasattr(self.current_loop, "chords"):
                for chord in self.current_loop.chords:
                    chord["chord"] = ""  # ou None si tu veux un vrai wipe
                    chord["degree"] = ""            
            Brint("[HARMONY] ⛔ Loop inactive (full range) → pas d'overlay harmonique")
            return
        if not self.is_loop_effectively_defined():
            self.harmony_canvas.delete("all")
            Brint("[HARMONY] ❌ Loop incomplète (A=0 ou B=duration) → overlay ignoré")
            return


        
        if not hasattr(self, "current_loop") or not self.current_loop:
            return
        # Comptage max pour normaliser la hauteur des colonnes de notes
        mapped_notes = getattr(self.current_loop, "mapped_notes", {})

        max_notes_count = max(len(notes) for notes in mapped_notes.values()) if mapped_notes else 1

        self.extend_chords_to_fit_loop()

        
        if not hasattr(self.current_loop, "mapped_notes"):
            Brint("[HARMONY WARN] mapped_notes manquant → recalcul")
            if hasattr(self, "grid_subdivs"):
                self.compute_mapped_notes()
            else:
                Brint("[HARMONY ERROR] Impossible de recalculer mapped_notes : pas de grid_subdivs")
                return

        
        canvas = self.harmony_canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        subdivision_mode = getattr(self, "subdivision_mode", None)

        subdivs_per_beat = self.get_subdivisions_per_beat(subdivision_mode)


        max_notes_per_subdiv = 6  # ← à ajuster si besoin
        # line_height = canvas_height / (subdivs_per_beat * max_notes_per_subdiv + 1)
        total_notes = sum(len(notes) for notes in self.current_loop.mapped_notes.values()) if hasattr(self.current_loop, "mapped_notes") else 1
        line_height = canvas_height / (total_notes + 1)
        
        
        if not hasattr(self, "current_loop") or not self.current_loop:
            pass#Brint("[HARMONY] ❌ Pas de boucle chargée")
            return

        chords = self.current_loop.chords
        if not chords:
            pass#Brint("[HARMONY] ❌ Aucun accord dans la boucle")
            return

        bpm = self.get_effective_bpm()
        loop_start_ms = self.current_loop.loop_start
        zoom = self.get_zoom_context()
        zoom_start = zoom["zoom_start"]
        zoom_end = zoom["zoom_end"]
        zoom_range = zoom["zoom_range"]



        Brint(f"[HARMONY DEBUG] zoom_start = {zoom_start:.1f} ms | zoom_end = {zoom_end:.1f} ms | zoom_range = {zoom_range:.1f} ms | canvas_width = {canvas_width}px")

        if canvas_width <= 10 or zoom_range <= 0:
            Brint("[HARMONY] ⏳ Canvas trop petit ou zoom invalide, retry dans 100ms")
            canvas.after(100, self.draw_harmony_grid_overlay)
            return

        DEGREE_COLOR_MAP = {
            "I":     "#ff0000",  # Rouge
            "ii":    "#ff9900",  # Orange clair
            "iii":   "#ffff00",  # Jaune
            "IV":    "#33cc33",  # Vert clair
            "V":     "#00cccc",  # Turquoise
            "vi":    "#3366ff",  # Bleu
            "vii°":  "#9900cc",  # Violet
            "?":     "#999999",  # Gris par défaut
        }

        display_mode = getattr(self, "harmony_chord_display_mode", "degree")

        # --- Optimization: avoid heavy redraw when nothing changed ---
        cache_key = (
            int(zoom_start),
            int(zoom_end),
            display_mode,
            getattr(self, "harmony_note_display_mode", "key"),
            round(bpm, 4),  # include tempo to invalidate cache when feathering
            hash(str(chords)),
            hash(str(getattr(self.current_loop, "mapped_notes", {}))),
        )
        if getattr(self, "_harmony_overlay_cache_key", None) == cache_key:
            # No change in zoom or data → skip redraw
            return
        self._harmony_overlay_cache_key = cache_key

        canvas.delete("all")

        Brint("[HARMONY] 🎼 Affichage harmonique basé sur loop.chords")

        for i, chord_data in enumerate(chords):
            if chord_data.get("autopad"):
                Brint(f"[HARMONY SKIP] Accord autopad ignoré : {chord_data}")
                continue

            
            beat_start = chord_data.get("beat_position", 0)
            beat_end = chord_data.get("beat_end")
            if beat_end is None and i + 1 < len(chords):
                beat_end = chords[i + 1].get("beat_position")
            if beat_end is None:
                beat_end = beat_start + 4  # fallback

            t_start_ms = loop_start_ms + (beat_start * 60.0 / bpm * 1000.0)
            t_end_ms = loop_start_ms + (beat_end * 60.0 / bpm * 1000.0)

            Brint(f"[HARMONY DEBUG] Beat {beat_start}–{beat_end} → t_start = {t_start_ms:.1f}ms, t_end = {t_end_ms:.1f}ms")

            x_start = self.time_sec_to_canvas_x(t_start_ms / 1000)
            x_end = self.time_sec_to_canvas_x(t_end_ms / 1000)
            x_center = (x_start + x_end) // 2

            info = self.current_loop.get_harmonic_info_by_measure(beat_start // 4)
            current_chord = info  # pour clarté

            
            if not info:
                Brint(f"[HARMONY DEBUG] ℹ️ Aucun degré pour beat {beat_start}")
                continue

            
            chord_label = chord_data.get("chord", "?")
            degree_label = info.get("degree", "?")

            # Texte affiché dans le rectangle (inchangé)
            if display_mode == "chord":
                label = chord_label
            elif display_mode == "both":
                label = f"{chord_label} / {degree_label}"
            else:
                label = degree_label

            # Couleur calée sur l'intervalle entre l'accord (root) et la key
            tonic = extract_tonic_from_chord(chord_label)
            interval, interval_label = get_interval_from_note(tonic, self.current_loop.key)
            color = INTERVAL_COLOR_MAP.get(interval, "#999999")
            Brint(f"[HARMONY RECTANGLE] Accord {chord_label} (tonique={tonic}) vs key {self.current_loop.key} → interval {interval} ({interval_label}) → color={color}")

            Brint(f"[HARMONY RECTANGLE] Accord {chord_label} vs key {self.current_loop.key} → interval {interval} ({interval_label}) → color={color}")
            Brint(f"[HARMONY] Rectangle {label} : x_start={x_start} → x_end={x_end} px (Δ={x_end - x_start})")

            # Rectangle avec contour coloré
            canvas.create_rectangle(x_start, 3, x_end, canvas_height-2,
                                    fill="", outline=color, width=2)

            # Texte accord en haut à gauche (plus petit)
            canvas.create_text(x_start + 3, 3,
                               text=label, fill=color,
                               anchor="nw", font=("Arial", 6, "bold"))

        # === Dessin des notes par subdivision harmonique ===
        if hasattr(self.current_loop, "mapped_notes"):
            Brint(f"[HARMONY DEBUG] mapped_notes keys = {list(self.current_loop.mapped_notes.keys())}")
        else:
            Brint("[HARMONY DEBUG] mapped_notes n'est pas encore initialisé")

        # === Dessin des notes par subdivision harmonique ===
        if hasattr(self.current_loop, "mapped_notes") and hasattr(self, "grid_subdivs"):
            # ✅ Correction : on aligne toutes les subdivisions sur le nombre max de notes
            notes_lists = []
            if hasattr(self.current_loop, "mapped_notes"):
                notes_lists = [n for n in self.current_loop.mapped_notes.values() if n and not all(isinstance(x, dict) and x.get("autopad") for x in n)]
            max_notes_per_subdiv = max((len(n) for n in notes_lists), default=0)

            # === Regrouper les subdivisions par mesure ===
            from collections import defaultdict

            subdivs_by_measure = defaultdict(list)
            measure_duration_ms = (60.0 / bpm) * 4 * 1000.0  # Durée d'une mesure en ms (4 temps)

            for i, (_, t_subdiv_sec) in enumerate(self.grid_subdivs):
                t_ms = t_subdiv_sec * 1000.0
                measure_idx = int((t_ms - loop_start_ms) / measure_duration_ms)
                subdivs_by_measure[measure_idx].append(i)

            # === Calcul du nombre max de subdivisions dans une mesure ===
            if not subdivs_by_measure:
                Brint("[HARMONY GRID ERROR] Aucun subdiv en mémoire — overlay annulé")
                return

            max_subdivs_in_measure = max(len(lst) for lst in subdivs_by_measure.values())
            Brint(f"[HARMONY ALIGN] max_subdivs_in_measure = {max_subdivs_in_measure}")

            # === Remplissage avec des slots vides (phantom) pour aligner toutes les colonnes ===
            for measure_idx, subdiv_list in subdivs_by_measure.items():
                initial = len(subdiv_list)
                while len(subdiv_list) < max_subdivs_in_measure:
                    subdiv_list.append(None)  # Slot phantom
                if len(subdiv_list) != initial:
                    Brint(f"[HARMONY ALIGN] ➕ Phantom slots ajoutés à la mesure {measure_idx} ({initial} → {len(subdiv_list)})")

            # Vérifie s'il y a au moins un hit avec status = 2
            has_confirmed_hits = any(
                getattr(self, "subdivision_state", {}).get(i, 0) == 2
                for i in self.current_loop.mapped_notes.keys()
            )
            if has_confirmed_hits:
                Brint("[HARMONY] 🔴 Mode filtré : seules les notes avec hit=2 seront affichées")


            for measure_idx, subdiv_indices in subdivs_by_measure.items():
                for local_pos, subdiv_index in enumerate(subdiv_indices):
                    if subdiv_index is None:
                        continue  # Phantom slot — ne rien dessiner

                    notes = self.current_loop.mapped_notes.get(subdiv_index, [])
                    if not notes:
                        continue

                    if subdiv_index >= len(self.grid_subdivs):
                        Brint(f"[HARMONY WARNING] subdiv_index {subdiv_index} > len(grid_subdivs) = {len(self.grid_subdivs)}")
                        continue

                    try:
                        t_subdiv_sec = self.grid_subdivs[subdiv_index][1]
                        t_subdiv_ms = t_subdiv_sec * 1000 

                        if not (zoom_start <= t_subdiv_ms <= zoom_end):
                            Brint(f"[HARMONY SKIP] Subdiv {subdiv_index} hors zoom : t={t_subdiv_ms:.1f}ms")
                            continue

                        x = self.time_sec_to_canvas_x(t_subdiv_ms / 1000.0)
                        Brint(f"[HARMONY DRAW] Subdiv {subdiv_index} → t={t_subdiv_sec:.3f}s | x={x} px | {len(notes)} note(s)")

                        # for i, note_data in enumerate(notes):
                        # Filtrage si mode hits confirmés activé
                        subdiv_hit_status = getattr(self, "subdivision_state", {}).get(subdiv_index, 0)

                        if has_confirmed_hits and subdiv_hit_status != 2:
                            continue  # On saute cette subdivision

                        filtered_notes = [n for n in notes if subdiv_hit_status == 2 or not has_confirmed_hits]
                        for i, note_data in enumerate(filtered_notes):
                            try:
                                note_str = note_data["note"]  # ✅ extraction du texte
                            except Exception as e:
                                Brint(f"[HARMONY NOTE ERROR] Note invalide dans subdiv {subdiv_index} → {note_data} ({e})")
                                continue
                            try:
                                note_label = note_str.lower()
                                note_mode = getattr(self, "harmony_note_display_mode", "key")

                                if note_mode == "absolute":
                                    display_text = note_label
                                    color = "#CCCCCC"
                                    interval_label = "–"  # Pas d'intervalle en absolu
                                elif note_mode == "key":
                                    interval, interval_label = get_interval_from_note(note_str, self.current_loop.key)
                                    display_text = f"{interval_label}"
                                    # display_text = f"{note_label} ({interval_label})"
                                    color = INTERVAL_COLOR_MAP.get(interval, "#999999")
                                elif note_mode == "chord":
                                    measure_info = self.current_loop.get_harmonic_info_by_measure(measure_idx)
                                    ref_chord = measure_info.get("chord") if measure_info else self.current_loop.key
                                    interval, interval_label = get_interval_from_note(note_str, ref_chord)
                                    display_text = f"{interval_label}"
                                    # display_text = f"{note_label} ({interval_label})"
                                    color = INTERVAL_COLOR_MAP.get(interval, "#999999")
                                else:
                                    display_text = note_label
                                    interval_label = "?"
                                    color = "#999999"

                                Brint(f"[HARMONY LABEL] Mode={note_mode} | {note_str} → {display_text} | Interval={interval_label} | Color={color}")

                            except Exception as e:
                                Brint(f"[HARMONY ERROR] get_interval_from_note({note_str}) → {e}")
                                display_text = note_label
                                interval_label = "?"
                                color = "#999999"

                            y = canvas_height * 0.5 + (i - max_notes_count / 2) * line_height

                            Brint(f"[HARMONY NOTE] Subdiv {subdiv_index} → {note_str} @ x={x:.1f}px, y={y:.1f}px | interval={interval_label} | color={color}")

                            # canvas.create_rectangle(x - 5, 5, x + 5, canvas_height - 5, outline="#333333", width=1)
                            # text_bbox_height = 12  # ajustable si besoin
                            # canvas.create_rectangle(
                                # x - 6, y - text_bbox_height / 2,
                                # x + 6, y + text_bbox_height / 2,
                                # outline="#333333", width=1
                            # )

                            canvas.create_text(
                                x + 3, y,
                                text=display_text,
                                fill=color,
                                font=("Courier", 8, "bold"),
                                anchor="nw"
                            )






                    except Exception as e:
                        Brint(f"[HARMONY NOTE DRAW ERROR] subdiv {subdiv_index} → {e}")
     
     
        Brint("[HARMONY] ✅ Fin du dessin harmonique")





    def tap_tempo(self):
        import time
        now = time.perf_counter()
        self.tap_times.append(now)
        if len(self.tap_times) > 8:
            self.tap_times.pop(0)

        if len(self.tap_times) >= 2:
            intervals = [self.tap_times[i+1] - self.tap_times[i] for i in range(len(self.tap_times)-1)]
            avg_interval = sum(intervals) / len(intervals)
            if avg_interval > 0:
                raw_bpm = 60.0 / avg_interval
                playback_rate = self.player.get_rate() if self.player else 1.0
                corrected_bpm = round(raw_bpm / playback_rate, 2)
                self.set_tempo_bpm(corrected_bpm, source="tap")
                Brint(f"[TAP TEMPO] 🧠 Raw BPM = {raw_bpm:.2f} | Playback rate = {playback_rate:.2f} → BPM corrigé = {corrected_bpm:.2f}")

    @property
    def loop_a(self):
        return self.loop_start / 1000.0 if self.loop_start is not None else None

    @property
    def loop_b(self):
        return self.loop_end / 1000.0 if self.loop_end is not None else None
        
        
    def on_timeline_resize(self, event):
        if self._resize_after_id is not None:
            self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(200, self._redraw_after_resize)

    def _redraw_after_resize(self):
        self._resize_after_id = None
        if self.player:
            self.needs_refresh = True
            self.refresh_static_timeline_elements()


if __name__ == "__main__":
    index = 0
    path = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.isdigit():
            index = int(arg)
        elif os.path.exists(arg):
            path = arg
        else:
            try:
                index = int(arg)
                Brint(f"[AUTOLOAD] ⚠️ Chemin '{arg}' introuvable, traité comme index {index}")
            except ValueError:
                Brint(f"[AUTOLOAD] ⚠️ Argument '{arg}' ignoré (ni index ni chemin valide)")
                index = 0

    root = tk.Tk()
    app = VideoPlayer(root, autoload_index=index, autoload_path=path)
    root.protocol("WM_DELETE_WINDOW", app.on_app_close)

    def run_for_5s():
        start = time.time()
        while time.time() - start < 5:
            app.update_playhead_by_time(app.player.get_time())  # 🔁 Utilise `app`, pas `player` ni `self`
            time.sleep(0.015)  # ~30 FPS

    # cProfile.runctx('run_for_5s()', globals(), locals(), filename='perf5s.stats')
    # pstats.Stats("perf5s.stats").sort_stats("cumtime").print_stats(30)

    root.mainloop()
