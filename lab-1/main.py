from classes.xml_controller import XMLController
from functions.utils import brute_force_xml_file_dir
from classes.page import Page

# Diretório do xml
XML_DIR_PATH = brute_force_xml_file_dir()

def first_task(xml_controller: XMLController):
    # Número de páginas
    num_of_pages = xml_controller.get_number_of_pages()
    print(f'Qtd páginas encontradas: {num_of_pages}')

def second_task(xml_controller: XMLController):
    # Lista de tuplas com id e título de cada página
    id_and_title = xml_controller.get_id_and_title_of_given_page()
    for id, title in id_and_title:
        print(f'ID: {id} - Title: {title}')

def third_task(xml_controller: XMLController):
    xml_controller.search_loop()

def main():
    xml_controller = XMLController(XML_DIR_PATH)
    second_task(xml_controller)

    
if __name__ == '__main__':
    main()