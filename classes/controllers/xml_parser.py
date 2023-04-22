from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as xml
from classes.models.page import Page
from typing import List, Dict, Literal


class XmlParser:
    root: Element
    query: str
    memoized_searches: Dict[int, List[Page]] = {}
    memoized_reverse_searches: Dict[List[Page], int] = {}

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
        self.memoized_reverse_searches = dict()

    def get_all_pages(self) -> List[Page]:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')

        # Traz todas as páginas
        pages = self.root.findall('page')

        # Retorna uma lista de páginas
        return list(map(lambda page: Page(page.find('id').text, page.find('title').text, page.find('text').text, 0), pages))

    def search_for_term(self, term: str, hash_method: Literal['reverse', 'default'] = 'default') -> list:
        # Se não houver root
        if not self.root:
            raise ValueError('self.root inválido ou não encontrado')
        # Se não houver termo
        if not term:
            raise ValueError('termo inválido ou não encontrado')

        if (hash_method == 'reverse'):
            # chave = lista de páginas, valor = hash do termo
            for k, v in self.memoized_reverse_searches.items():
                if v == hash(term):
                    print('Hash invertido')
                    return sorted(k, reverse=True)
        else:
            if hash(term) in self.memoized_searches:
                print('Hash padrao')
                return sorted(self.memoized_searches[hash(term)], reverse=True)

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
                temp_page = Page(page.id, page.title, page.text,
                                 count * 2 if isOnTitle else count)
                included.append(temp_page)
        result = sorted(included, reverse=True)

        self.memoize_search(term, result)

        return sorted(included, reverse=True)

    def get_memorized_searches(self) -> dict:
        return self.memoized_searches

    def memoize_search(self, term: str, pages: List[Page], method: Literal['reverse', 'default'] = 'default') -> None:
        if method == 'default':
            self.memoized_searches[hash(term)] = pages
        else:
            self.memoized_reverse_searches[pages] = hash(term)
        pass
