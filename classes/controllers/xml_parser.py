from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from classes.models.page import Page
from typing import List, Dict, Literal, Set
import time


class XmlParser:
    root: Element
    pages: List[Page]
    query: str
    memo: Dict[str, List[Page]]

    def __init__(self, xml_dir: str) -> None:
        self.load_xml(xml_dir)
        self.query = ''
        self.pages = []

    def filter_page_content(self, page_content: List[str], withSet: bool) -> List[str]:
        words_with_min_size = list(
            filter(lambda word: len(word) >= 4, page_content))

        if withSet:
            result = list(set(
                map(lambda word: word.lower(), words_with_min_size)))
        else:
            result = list(map(lambda word: word.lower(), words_with_min_size))
        return result

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
            # Divide o título e o texto em palavras NÃO repetidas
            key_title_words = self.filter_page_content(
                page.title.split(), True)
            key_text_words = self.filter_page_content(page.text.split(), True)

            all_key_words = list(key_title_words + key_text_words)

            # Divide o título e o texto em palavras repetidas
            all_possible_title_words = self.filter_page_content(
                page.title.split(), False)
            all_possible_text_words = self.filter_page_content(
                page.text.split(), False)

            for word in all_key_words:
                # Conta quantas vezes a palavra aparece no título
                count_on_title = all_possible_title_words.count(word)

                # Conta quantas vezes a palavra aparece no texto
                count_on_body = all_possible_text_words.count(word)

                # Se a palavra estiver no título, ou seja, relevância maior
                onTitle = count_on_title > 0

                # Se a palavra estiver no título, a relevância é maior(2x) se não for, a relevância continua a mesma
                relevance = (count_on_title + count_on_body + page.relevance) * \
                    2 if onTitle else count_on_title + count_on_body + page.relevance

                # Relenvância normal
                raw_relevance = count_on_title + count_on_body + page.raw_relevance

                # Se a palavra não estiver no dicionário, adicione-a
                if word not in self.memo.keys():
                    self.memo[word] = []

                # Se a palavra estiver no título ou no corpo
                if count_on_title > 0 or count_on_body > 0:
                    # Instancia uma nova página com a relevância calculada
                    new_page = Page(page.id, page.title, page.text,
                                    relevance, raw_relevance)
                    # Adiciona a página no dicionário
                    self.memo[word].append(new_page)

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
        return result
        # return sorted(result, key=lambda page: page.relevance, reverse=True)
