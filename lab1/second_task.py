from classes.xml_parser import XmlParser

def second_task(xml_controller: XmlParser):
    # Lista de tuplas com id e título de cada página
    id_and_title = xml_controller.get_id_and_title_of_given_page()
    for id, title in id_and_title:
        print(f'ID: {id} - Title: {title}')


