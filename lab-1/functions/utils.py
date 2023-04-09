import os
import time

folder_path = './../'

def brute_force_xml_file_dir() -> str:
    # Recursivamente percorre a árvore de diretórios até achar o arquivo data.xml
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == 'data.xml':
                # Found data.xml file, open it
                file_path = os.path.join(root, file)
                return file_path
    return ''

def clear_screen() -> None:
    # Limpa a tela
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time() -> str:
    # Retorna a data e hora atual
    now = time.localtime()
    # Formata a data e hora
    formatted_time = time.strftime("%d-%m-%y %H:%M", now)
    return formatted_time