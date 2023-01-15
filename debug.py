import os

from anki.cards import Card
from aqt import gui_hooks


def log(text: str, filename: str):
    with open(os.path.join(os.path.dirname(__file__), filename), 'a', encoding='utf8') as f:
        f.write(text + '\n')


def log_card_htmls():
    def card_will_show(text: str, card: Card, kind: str) -> str:
        log(text, 'log_card_htmls.html')
        return text
    gui_hooks.card_will_show.append(card_will_show)


