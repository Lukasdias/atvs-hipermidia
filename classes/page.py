import textwrap
from termcolor import colored


class Page:
    id: str
    title: str
    text: str
    count_of_term_in_text: int
    weight: int

    def __init__(self, id: str , title: str, text: str, count_of_term_in_text: int, weight: int) -> None:
        if id is None or title is None or text is None:
            raise ValueError(
                'id, title e/ou text inválido(s) ou não encontrado(s)')
        self.id = id
        self.title = title
        self.text = text
        self.count_of_term_in_text = count_of_term_in_text
        self.weight = weight

    def __str__(self) -> str:
        colored_text = colored(self.title, 'green', attrs=['bold'])
        peso_text = colored(str(self.weight), 'red', attrs=['bold'])
        return f'ID: {self.id}\nTitulo: {colored_text}\nPeso: {peso_text}\nContador termo: {self.count_of_term_in_text}\n'

    def __dict__(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'count_of_term_in_text': self.count_of_term_in_text
        }

    def print_page_with_colored_given_term(self, term: str) -> None:
        # colored_text = self.text.replace(
        #     term, colored(term, 'green', attrs=['bold']))
        # print(f'-- ID: {self.id}\nTitle: {self.title}\nText: {colored_text}\n')
        print(f'ID: {self.id}\nTitle: {self.title}')


export = Page
