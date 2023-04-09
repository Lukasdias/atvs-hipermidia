from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from functions.utils import clear_screen, get_current_time
from enum import Enum, auto
from classes.page import Page
from typing import List


class XMLController:
    class MenuOptions(Enum):
        IDLE = auto()
        SEARCH = auto()
        SEE_PREVIOUS_SEARCHES = auto()
        CLEAR_SCREEN = auto()
        EXIT = auto()

    root: Element
    query: str
    memoized_searches: dict
    current_menu_option: MenuOptions

    def __init__(self, xml_dir: str) -> None:
        self.load_xml(xml_dir)
        self.current_menu_option = XMLController.MenuOptions.IDLE
        self.query = ''

    def load_xml(self, xml_dir: str) -> None:
        # Se não houver xml_dir, retorne 0
        if not xml_dir:
            raise ValueError('diretório do xml inválido ou não encontrado')
        # Carrega o xml
        tree = xml.parse(xml_dir)
        # Agora o root corresponde ao xml
        self.root = tree.getroot()
        self.memoized_searches = dict()

    def get_number_of_pages(self) -> int:
        # Se não houver page, retorne 0
        if not self.root:
            raise ValueError('xml_root inválido ou não encontrado')
        # Retorna o número de páginas
        pages = self.root.findall('page')
        return len(pages)

    def get_all_refs_of_given_tag_from_file(self, tag: str) -> list:
        # Se não houver page, retorne 0
        if not self.root:
            raise ValueError('xml_root inválido ou não encontrado')
        if not tag:
            raise ValueError('tag inválida ou não encontrada')

        # Retorna uma lista com o conteúdo da tag
        searched_tag = []
        for page in self.root:
            # Se não houver a tag, retorne uma string vazia
            if page.find(tag) is None:
                searched_tag.append('')
                continue
            # Se houver, retorne o conteúdo da tag
            target_text = page.find(tag).text
            searched_tag.append(target_text)
        return searched_tag

    def get_id_and_title_of_given_page(self) -> list:
        # Utilizando a funcão anterior para reduzir o código
        ids = self.get_all_refs_of_given_tag_from_file('id')
        titles = self.get_all_refs_of_given_tag_from_file('title')

        # Função zip combina duas listas ou mais em uma lista de tuplas
        return list(zip(ids, titles))

    def search_loop(self) -> None:
        while True:
            self.render_idle()
            if self.current_menu_option == XMLController.MenuOptions.SEARCH:
                self.render_search()
            elif self.current_menu_option == XMLController.MenuOptions.SEE_PREVIOUS_SEARCHES:
                self.render_previous_searches()
            elif self.current_menu_option == XMLController.MenuOptions.CLEAR_SCREEN:
                clear_screen()
            elif self.current_menu_option == XMLController.MenuOptions.EXIT:
                break

    def search_for_term(self, term: str) -> list:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')
        # Se não houver termo
        if not term:
            raise ValueError('termo inválido ou não encontrado')

        # Lista de resultados
        included = list()
        for elem in self.root:
            if (elem.tag == 'page'):
                for sub_elem in elem:
                    page = Page(elem.find('id').text, elem.find(  # type: ignore
                        'title').text, elem.find('text').text)  # type: ignore
                    if sub_elem.tag == 'title' and term in sub_elem.text:  # type: ignore
                        included.append(page)
        return included

    def render_idle(self) -> None:
        print("Tarefa 1 - XML Parser")
        print("1. Opção 1 - Pesquisar")
        print("2. Opção 2 - Ver pesquisas anteriores")
        print("3. Opção 3 - Limpar tela")
        print("4. Opção 4 - Sair")

        input_value = input()

        if input_value == '1':
            self.current_menu_option = XMLController.MenuOptions.SEARCH
        elif input_value == '2':
            self.current_menu_option = XMLController.MenuOptions.SEE_PREVIOUS_SEARCHES
        elif input_value == '3':
            self.current_menu_option = XMLController.MenuOptions.CLEAR_SCREEN
        elif input_value == '4':
            self.current_menu_option = XMLController.MenuOptions.EXIT
        else:
            print('Opção inválida')
            self.current_menu_option = XMLController.MenuOptions.IDLE

    def render_search(self) -> None:
        temp = input('Digite o termo que deseja pesquisar: ')
        if temp == 'sair':
            self.current_menu_option = XMLController.MenuOptions.IDLE
        elif temp == '':
            print('Termo inválido')
        else:
            # Pesquisa o termo
            self.query = temp
            self.current_menu_option = XMLController.MenuOptions.SEARCH

            # Verifica se a pesquisa já foi realizada
            if self.query in self.memoized_searches:
                print(
                    f'Foram encontradas {len(self.memoized_searches[self.query][0])} ocorrências do termo "{self.query}"')
                print(f"Resultados: ")
                for page in self.memoized_searches[self.query][0]:
                    print(page.__str__())
                return
            else:
                result: List[Page] = self.search_for_term(self.query)

            # Cacheia o resultado em um dicionário
            self.memoized_searches[self.query] = [result, get_current_time()]

            # Imprime o resultado
            if result:
                print(
                    f'Foram encontradas {len(result)} ocorrências do termo "{self.query}"')
                print(f"Resultados: ")
                for page in result:
                    print(page.__str__())
            else:
                print(
                    f'Não foram encontradas ocorrências do termo "{self.query}"')

        # Verificar se é a primeira pesquisa
        is_first_search = len(self.memoized_searches) == 0
        if not is_first_search:
            print()
            is_first_search = False

    def render_previous_searches(self) -> None:
        if not self.memoized_searches:
            print('Nenhuma pesquisa foi realizada')
            return

        for query, result in self.memoized_searches.items():
            print(
                f'Pesquisa: {query}, Qtd de resultados: {len(result[0])} ---- Horário da pesquisa: {result[1]}')
