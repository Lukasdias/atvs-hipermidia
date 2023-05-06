from termcolor import colored


class Page:
    id: str
    title: str
    text: str
    relevance: int
    raw_relevance: int

    def __init__(self, id: str, title: str, text: str, relevance: int, raw_relevance: int) -> None:
        if id is None or title is None or text is None:
            raise ValueError(
                'id, title e/ou text inválido(s) ou não encontrado(s)')
        self.id = id
        self.title = title
        self.text = text
        self.relevance = relevance
        self.raw_relevance = raw_relevance

    def add_relevance(self, relevance: int) -> None:
        self.relevance += relevance

    def add_raw_relevance(self, raw_relevance: int) -> None:
        self.raw_relevance += raw_relevance

    def __str__(self) -> str:
        red_text = colored(f"{self.relevance}", 'blue',
                           attrs=['bold', 'blink'])
        return f'ID: {self.id}\nTitulo: {self.title}\nRelevancia: {red_text}\n Texto: {self.text[:100]}...\n'

    def __dict__(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'relevance': self.relevance,
            'raw_relevance': self.raw_relevance
        }

    def __lt__(self, other: object):
        if isinstance(other, Page):
            return self.relevance < other.relevance
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Page):
            return self.id == other.id
        return False


export = Page
