from classes.xml_parser import XmlParser
from classes.page import Page


def first_task(xml_controller: XmlParser):
    # Número de páginas
    num_of_pages = xml_controller.get_number_of_pages()
    print(f'Qtd páginas encontradas: {num_of_pages}')
