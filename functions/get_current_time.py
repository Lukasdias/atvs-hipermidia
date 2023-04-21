import time

def get_current_time() -> str:
    # Retorna a data e hora atual
    now = time.localtime()
    # Formata a data e hora
    formatted_time = time.strftime("%d-%m-%y %H:%M", now)
    return formatted_time