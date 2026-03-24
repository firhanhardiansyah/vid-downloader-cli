import os
import re

def ensure_folder(folder):
    os.makedirs(folder, exist_ok=True)

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)