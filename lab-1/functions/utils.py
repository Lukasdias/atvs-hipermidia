import os
import time

folder_path = './../'

def brute_force_xml_file_dir() -> str:
    # Recursively search for data.xml file
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == 'data.xml':
                # Found data.xml file, open it
                file_path = os.path.join(root, file)
                return file_path

def clear_screen() -> None:
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time() -> str:
    now = time.localtime()
    formatted_time = time.strftime("%d-%m-%y %H:%M", now)
    return formatted_time