
from typing import List
from classes.page import Page

def count_ocurrences_of_subtring_in_string(string: str, substring: str):
    lower_string = string.lower()
    lower_substring = substring.lower()
    return lower_string.count(lower_substring)


def order_pages_by_weight(pages: List[Page]):
    return sorted(pages, key=lambda page: page.weight, reverse=True)

