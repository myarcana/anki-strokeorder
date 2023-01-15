import os

from anki import hooks
from anki.cards import Card
from anki.template import TemplateRenderContext
from aqt import gui_hooks

from .render import get_steps, get_unified


def _write(text: str, filename: str):
    with open(os.path.join(os.path.dirname(__file__), filename), 'a', encoding='utf8') as f:
        f.write(text + '\n')


def strokeorder_field_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: TemplateRenderContext
) -> str:
    prefix = 'strokeorder-'
    if not filter_name.startswith(prefix):
        return field_text
    function = filter_name[len(prefix):]
    if function == "steps":
        steps = get_steps(field_text)
        return steps
    elif function == "unified":
        unified = get_unified(field_text)
        return unified
    else:
        return invalid_name(filter_name)


def invalid_name(filter_name: str) -> str:
    return f"invalid filter name: {filter_name}"

hooks.field_filter.append(strokeorder_field_filter)

