from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from classes.models.page import Page
from typing import List, Dict, Literal
import json
import os


def make_page(element: Element) -> Page:
    # Se não houver elemento
    if not element:
        raise ValueError('elemento inválido ou não encontrado')

    # Retorna uma página
    return Page(
        element.find('id').text,
        element.find('title').text,
        element.find('text').text, 0, 0)


class XmlParser:
    root: Element
    pages: List[Page]
    query: str
    memo: Dict[str, Dict[str, Page]]

    def __init__(self, xml_dir: str) -> None:
        self.load_xml(xml_dir)
        self.query = ''
        self.pages = []

    def load_xml(self, xml_dir: str) -> None:
        # Se não houver xml_dir, retorne 0
        if not xml_dir:
            raise ValueError('diretório do xml inválido ou não encontrado')

        # Carrega o xml
        tree = xml.parse(xml_dir)

        # Agora o root corresponde ao xml
        self.root = tree.getroot()
        self.pages = self.get_all_pages()
        self.memo = dict()

        self.fill_possible_words()

    def fill_possible_words(self):
        for page in self.pages:
            # Palavras dentro do título = 2x relevância
            words_inside_title_of_page = page.title.split()

            # Palavras dentro do texto = 1x relevância
            words_inside_text_of_page = page.text.split()

            # Todas as palavras presentes na página atual
            all_words = words_inside_title_of_page + words_inside_text_of_page

            filtered_words = list(
                filter(lambda word: len(word) >= 4, all_words))

            filtered_and_mapped_words = list(map(lambda word: word.lower()[
                :-1] if word.endswith('s') else word.lower(), filtered_words))

            # Para cada palavra na lista de palavras filtradas
            for word in filtered_and_mapped_words:
                # Conta quantas vezes a palavra aparece no título e no texto
                count_on_title = page.title.count(word)
                count_on_text = page.text.count(word)
                count = count_on_title + count_on_text
                # Se a palavra estiver no título, a relevância é dobrada
                isOnTitle = count_on_title > 0
                relevance = 2 * count if isOnTitle else count
                # Cria uma nova página com a relevância e a quantidade de vezes que a palavra aparece
                new_page = Page(page.id, page.title,
                                page.text, relevance, count)
                # Se a palavra já estiver no dicionário, adicione a página
                if word in self.memo.keys():
                    self.memo[word][page.id] = new_page
                # Senão, crie uma nova chave e adicione a página
                else:
                    self.memo[word] = dict()
                    self.memo[word][page.id] = new_page

    def get_all_pages(self) -> List[Page]:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')

        # Traz todas as páginas
        unparsed_pages = self.root.findall('page')

        # Retorna uma lista de páginas
        pages = list(
            map(
                lambda page: Page(
                    page.find('id').text,
                    page.find('title').text,
                    page.find('text').text, 0, 0), unparsed_pages))

        return pages

    def search_for_term(
        self,
        term: str,
    ) -> List[Page]:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')
        # Se não houver termo
        if not term:
            raise ValueError('termo inválido ou não encontrado')

        # Lista de resultados
        included: List[Page] = []

        # Se o termo estiver no dicionário
        if term in self.memo.keys():
            # Adicione todos os valores do dicionário na lista de resultados
            for value in self.memo[term].values():
                included.append(value)

        result = sorted(included)

        # Percorre todas as páginas
        # for page in self.pages:
        #     count = page.text.lower().count(term.lower())
        #     isOnTitle = page.title.lower().count(term.lower()) > 0
        #     if count > 0:
        # Multiplique a relevância por 2 se o termo estiver no título
        #         temp_page = Page(page.id, page.title, page.text,
        #                          count * 2 if isOnTitle else count, count)
        #         included.append(temp_page)
        # result = sorted(included)

        return result
