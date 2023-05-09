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

    def load_xml(self, xml_dir: str) -> None:
        # Se não houver xml_dir, retorne 0
        if not xml_dir:
            raise ValueError('diretório do xml inválido ou não encontrado')

        print(f'Parseando {xml_dir}...')
        # Carrega o xml
        tree = xml.parse(xml_dir)

        # Agora o root corresponde ao xml
        self.root = tree.getroot()
        # Carrega todas as páginas
        self.pages = self.get_all_pages()
        # Inicializa o dicionário
        self.memo = defaultdict(list)

        # Inicia o cronômetro
        load_start = time.time()
        print(f'Carregando {len(self.pages)} páginas...')

        self.memoize_all_queries()

        # Finaliza o cronômetro
        load_end = time.time()

        running_time = load_end - load_start

        # Formata o tempo de carregamento
        # Se o tempo for menor que 1, multiplique-o por 1000 e adicione 'ms' no final
        # Caso contrário, apenas adicione 's' no final
        format_time = round(
            running_time * 1000 if running_time < 1 else running_time, 2)

        format_sufix = 'ms' if running_time < 1 else 's'

        print(f'Carregamento concluído em: {format_time}{format_sufix}!')

    # Retorna um dicionário com todas as palavras e suas respectivas frequências
    def get_all_verbetes_words(self, page_content: List[str]) -> DefaultDict[str, int]:
        words_dict: DefaultDict[str, int] = defaultdict(int)
        # Se a palavra tiver mais de 4 caracteres, adicione-a ao dicionário
        words_list = list(
            filter(lambda word: len(word) >= 4, page_content))
        for word in words_list:
            # Se a palavra já estiver no dicionário, incremente-a, caso contrário, adicione-a
            # default dict vai incrementar automaticamente, pois o valor padrão é 0
            words_dict[word] += 1
        return words_dict

    # Cria um dicionário com todas as palavras e suas respectivas páginas
    def memoize_all_queries(self):
        for page in self.pages:
            # Pega todas as palavras da página, sem distinção entre título e texto
            words = self.get_all_verbetes_words(
                page.text.split() + page.title.split())
            for word in words:
                # Se a palavra estiver no título, seu peso é 2, caso contrário, 1
                weight = 2 if page.title.count(word) > 0 else 1
                new_page = Page(page.id, page.title, page.text,
                                words[word] * weight, words[word])
                # Se a página não estiver no dicionário, adicione-a
                self.memo[word].append(new_page)

    # Parseia o xml e retorna uma lista de páginas já instanciadas
    def get_all_pages(self) -> List[Page]:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')

        # Traz todas as páginas
        unparsed_pages = self.root.findall('page')

        # Retorna uma lista de páginas
        # map() aplica uma função a cada elemento de uma lista
        # nessa caso a função é uma lambda que retorna uma página
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

        # Se o termo terminar com 's', remova o 's'
        # Ex: 'carros' -> 'carro'
        # Porém, se o termo não terminar com 's', apenas deixe-o em minúsculo
        # Mas por que isso?
        # O resultado de 'carros' deve ser a soma dos resultados de 'carro' e 'carros'
        parse_term = term.lower()[:-1] if term.endswith('s') else term.lower()

        # Se o termo estiver no dicionário
        if term in self.memo.keys():
            # Adicione todos os valores do dicionário na lista de resultados
            if term.endswith('s'):
                # Resultado de 'carros' = resultado de 'carro' + resultado de 'carros'
                result = self.memo[parse_term] + self.memo[term]
            else:
                # Resultado de 'carro' = resultado de 'carro'
                result = self.memo[term]
        # Ordena a lista de resultados por relevância de forma crescente
        return sorted(result, key=lambda page: page.relevance, reverse=False)
