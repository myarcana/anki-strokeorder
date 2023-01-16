from anki import hooks
from anki.template import TemplateRenderContext

from . import debug
from .render import get_steps, get_unified


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


