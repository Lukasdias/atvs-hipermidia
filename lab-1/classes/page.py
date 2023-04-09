import textwrap
from termcolor import colored


class Page:
    id: str
    title: str
    text: str

    def __init__(self, id: str or None, title: str or None, text: str or None) -> None:
        if id is None or title is None or text is None:
            raise ValueError(
                'id, title e/ou text inválido(s) ou não encontrado(s)')
        self.id = id
        self.title = title
        self.text = text

    def __str__(self) -> str:
        short_text = textwrap.fill(self.text, width=80)
        colored_text = colored(short_text, 'green', attrs=['bold'])
        # return f'-- ID: {self.id}\nTitle: {self.title}\nText: {colored_text}\n'
        return f'ID: {self.id}\nTitle: {self.title} /\n '

    def __dict__(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text
        }

    def print_page_with_colored_given_term(self, term: str) -> None:
        # colored_text = self.text.replace(
        #     term, colored(term, 'green', attrs=['bold']))
        # print(f'-- ID: {self.id}\nTitle: {self.title}\nText: {colored_text}\n')
        print(f'ID: {self.id}\nTitle: {self.title}')


export = Page
