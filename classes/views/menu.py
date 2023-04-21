from enum import Enum
from termcolor import colored
from typing import List
from classes.models.page import Page
from classes.controllers.xml_parser import XmlParser

import os

class Menu:
    class MenuOptions(Enum):
        IDLE = 0
        SEARCH = 1
        CLEAR_SCREEN = 2
        EXIT = 3

    xml_parser: XmlParser

    def __init__(self, xml_parser: XmlParser):
        self.current_menu_option = 0
        self.xml_parser = xml_parser

    def print_menu(self):
        print("\\ Verbetes Wikipedia //")
        print("1. Opção 1 - Pesquisar")
        print("2. Opção 2 - Limpar tela")
        print("3. Opção 3 - Sair")

    def get_user_input(self):
        return input()

    def process_user_input(self, input_value):
        if input_value == '1':
            self.current_menu_option = Menu.MenuOptions.SEARCH
        elif input_value == '2':
            self.current_menu_option = Menu.MenuOptions.EXIT
        else:
            print('Opção inválida')
            self.current_menu_option = Menu.MenuOptions.IDLE

    def run_menu(self):
        while True:
            self.print_menu()
            input_value = self.get_user_input()
            self.process_user_input(input_value)
            if self.current_menu_option == Menu.MenuOptions.SEARCH:
                self.render_search()
                pass
            elif self.current_menu_option == Menu.MenuOptions.EXIT:
                # sair do programa
                break

    def render_search(self):
        # renderizar a tela de pesquisa
        print('Digite o termo que deseja pesquisar: ')
        termo = input()
        pages = self.xml_parser.search_for_term(termo)
        self.render_search_results(pages)
        pass


    def render_search_results(self, pages: List[Page]):
        # renderizar os resultados da pesquisa
        print('Resultados da pesquisa:')
        for page in pages:
            print(page.__str__())
        pass

    def clean_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')