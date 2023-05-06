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
        titulo = colored("<", "green", attrs=[
                         "blink"]) + " Verbetes Wikipedia " + colored("/>", "green", attrs=["blink"])
        print(titulo)
        print(f"{colored('1', 'blue')}. Opção 1 - Pesquisar")
        print(f"{colored('2', 'yellow')}. Opção 2 - Limpar tela")
        print(f"{colored('3', 'cyan')}. Opção 3 - Sair")

    def get_user_input(self):
        return input()

    def process_user_input(self, input_value):
        if input_value == '1':
            self.current_menu_option = Menu.MenuOptions.SEARCH
        elif input_value == '2':
            self.current_menu_option = Menu.MenuOptions.CLEAR_SCREEN
        elif input_value == '3':
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
                # renderizar a tela de pesquisa
                self.render_search()
                pass
            elif self.current_menu_option == Menu.MenuOptions.CLEAR_SCREEN:
                # limpar a tela
                self.clean_screen()
            elif self.current_menu_option == Menu.MenuOptions.EXIT:
                # sair do programa
                break

    def render_search(self):
        # renderizar a tela de pesquisa
        print('Digite o termo que deseja pesquisar: ')
        termo = input()
        if (len(termo) < 4):
            print('Termo possui menos de 4 caracteres, tente outro com +4 caracteres')
            return
        termo_sem_radical = ''

        if termo[len(termo) - 1] == 's':
            termo_sem_radical = termo[:-1]

        if (termo_sem_radical != ''):
            p_sem_radical = self.xml_parser.search_for_term(termo_sem_radical)
            p_com_radical = self.xml_parser.search_for_term(termo)
            pages = p_com_radical + p_sem_radical

        else:
            pages = self.xml_parser.search_for_term(termo)

        self.render_search_results(pages)
        pass

    def render_search_results(self, pages: List[Page]):
        # renderizar os resultados da pesquisa
        if (len(pages) == 0):
            print('Nenhum resultado encontrado')
            return

        # Número de páginas
        # num_pages = len(self.xml_parser.memo.values())
        # print(f"Total de páginas: {num_pages}")

        print(
            f'Foram encontrados resultados em {len(pages)} páginas diferentes')

        total = 0
        for page in pages:
            total = page.raw_relevance + total
        print(f'Qtd de citacoes pesquisa: {total}')

        # for page in pages:
        #     print(page.__str__())

    def clean_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
