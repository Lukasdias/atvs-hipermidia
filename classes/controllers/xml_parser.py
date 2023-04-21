from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from functions.utils import clear_screen, get_current_time
from enum import Enum, auto
from classes.models.page import Page
from typing import List, Dict, Optional


class XmlParser:

    root: Element
    query: str
    memoized_searches: Dict[str, Page] = {}

    def __init__(self, xml_dir: str) -> None:
        self.load_xml(xml_dir)
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

    def get_all_pages(self) -> List[Page]:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')

        # Traz todas as páginas
        pages = self.root.findall('page')

        # Retorna uma lista de páginas
        return list(map(lambda page: Page(page.find('id').text, page.find('title').text, page.find('text').text, 0), pages))

    def get_all_refs_of_given_tag_from_file(self, tag: str) -> list[str]:
        # Se não houver page, retorne 0
        if not self.root:
            raise ValueError('xml_root inválido ou não encontrado')
        if not tag:
            raise ValueError('tag inválida ou não encontrada')
        # Traz todas as páginas
        pages = self.root.findall('page')
        # Filtra as páginas que contém a tag
        tags = filter(lambda page: page.find(tag) is not None, pages)
        # Retorna uma lista com o texto da tag
        return list(map(lambda page: page.find(tag).text, tags)) # type: ignore

    def search_for_term(self, term: str,  tag= 'title') -> list:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')
        # Se não houver termo
        if not term:
            raise ValueError('termo inválido ou não encontrado')

        # Lista de resultados
        included: List[Page] = []

        pages = self.get_all_pages()

        # Número de páginas
        num_pages = len(pages)
        print(f"Total de páginas: {num_pages}")

        # Percorre todas as páginas
        for page in pages:
            count = page.text.lower().count(term.lower())
            isOnTitle = page.title.lower().count(term.lower()) > 0
            if count > 0:
                # Multiplique a relevância por 2 se o termo estiver no título
                if isOnTitle:
                    count *= 2
                temp_page = Page(page.id, page.title, page.text, count * 2 if isOnTitle else count)
                included.append(temp_page)
        result = sorted(included, reverse=True)

        self.memoized_searches[term] = result[0] if len(result) > 0 else None
        
        return sorted(included, reverse=True)


    def get_memorized_searches(self) -> dict:
        return self.memoized_searches
