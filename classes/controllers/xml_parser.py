from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from classes.models.page import Page
from typing import List, Dict, Literal, Set, DefaultDict
import time
from collections import defaultdict


class XmlParser:
    root: Element
    pages: List[Page]
    query: str
    memo: DefaultDict[str, List[Page]]

    def __init__(self, xml_dir: str) -> None:
        self.load_xml(xml_dir)
        self.query = ''
        self.pages = []

    def filter_page_content(self, page_content: List[str], weight: int) -> DefaultDict[str, int]:
        dict:DefaultDict[str, int]  = defaultdict()
        words_with_min_size = list(
            filter(lambda word: len(word) >= 4, page_content))
        for word in words_with_min_size:
            if word in dict.keys():
                dict[word] += 1 * weight
            else:
                dict[word] = 0
        return dict


    def load_xml(self, xml_dir: str) -> None:
        # Se não houver xml_dir, retorne 0
        if not xml_dir:
            raise ValueError('diretório do xml inválido ou não encontrado')

        print(f'Parseando {xml_dir}...')
        # Carrega o xml
        tree = xml.parse(xml_dir)

        # Agora o root corresponde ao xml
        self.root = tree.getroot()
        self.pages = self.get_all_pages()
        self.memo = dict()

        load_start = time.time()
        print(f'Carregando {len(self.pages)} páginas...')
        self.fill()
        load_end = time.time()

        running_time = load_end - load_start

        format_time = round(
            running_time * 1000 if running_time < 1 else running_time, 2)

        format_sufix = 'ms' if running_time < 1 else 's'

        print(f'Carregamento concluído em: {format_time}{format_sufix}!')

    def fill(self):
        for page in self.pages:
            words = self.filter_page_content(page.text.split() + page.title.split(), 1)
            for word in words:
                if word in self.memo.keys():
                    weight = 2 if page.title.count(word) > 0 else 1
                    new_page = Page(page.id, page.title, page.text, words[word] * weight, words[word])
                    self.memo[word].append(new_page)
                else:
                    self.memo[word] = []

            # for word in words.keys():
            #     if word not in self.memo.keys():
            #         self.memo[word] = []
            #     # Se a palavra estiver no título ou no corpo
            #     if words[word] > 0:
            #         # Instancia uma nova página com a relevância calculada
            #         new_page = Page(page.id, page.title, page.text,
            #                         words[word], words[word])
            #         # Adiciona a página no dicionário
            #         self.memo[word].append(new_page)

    # Parseia o xml e retorna uma lista de páginas já instanciadas
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
        result: List[Page] = []

        parse_term = term.lower()[:-1] if term.endswith('s') else term.lower()

        # Se o termo estiver no dicionário
        if term in self.memo.keys():
            # Adicione todos os valores do dicionário na lista de resultados
            if term.endswith('s'):
                result = self.memo[parse_term] + self.memo[term]
            else:
                result = self.memo[term]
        # return result
        return sorted(result, key=lambda page: page.relevance, reverse=False)
