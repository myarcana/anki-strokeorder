from itertools import accumulate

from .stroke_data import StrokeData, get_stroke_data


CELL_WIDTH = CELL_HEIGHT = 1024
UPPER_LEFT = (0, 900)


def _indent(block: str) -> str:
    return '  ' + '\n  '.join(block.splitlines())


def _make_container(cols: int, rows: int, groups: list[str]) -> str:
    width = CELL_WIDTH * cols
    height = CELL_HEIGHT * rows
    content = '\n'.join(groups)
    svg = fr'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="max-width: calc(1em * {cols});">
{_indent(content)}
</svg>
'''.strip()
    return svg


def _make_group(col: int, row: int, paths: list[str]) -> str:
    x = col * CELL_WIDTH + UPPER_LEFT[0]
    y = - row * CELL_HEIGHT - UPPER_LEFT[1]
    content = '\n'.join(paths)
    g = fr'''
<g transform="scale(1, -1) translate({x}, {y})">
{_indent(content)}
</g>
'''.strip()
    return g

def _make_text(col: int, row: int, character: str) -> str:
    x = col * CELL_WIDTH + UPPER_LEFT[0]
    y = - row * CELL_HEIGHT - UPPER_LEFT[1]
    foreign_object = fr'''
<text x="{x}" y="{y}" style="font-size: {CELL_HEIGHT}px;">{character}</text>
'''.strip()
    return foreign_object


def _make_path(definition: str, style: dict[str, str]) -> str:
    path = fr'''
<path d="{definition}" style="{' '.join(f'{prop}: {value};' for prop, value in style.items())}"></path>
'''.strip()
    return path


def _style_stroke_border(color: str, width: str) -> dict[str, str]:
    return {
        "stroke": color,
        "stroke-width": width,
        "stroke-linejoin": "round",
        "paint-order": "stroke"
    }


def _style_stroke_fill(color: str) -> dict[str, str]:
    return {
        "fill": color
    }


def _opacity(opacity: str) -> dict[str, str]:
    return {
        "opacity": opacity
    }


def get_unified(word: str) -> str:
    characters = list(word)
    stroke_data = get_stroke_data(characters)
    groups = []
    path_style = _style_stroke_fill('currentColor') | _style_stroke_border('#333', '30px')
    for i, stroke_datum in enumerate(stroke_data):
        if stroke_datum is None:
            groups.append(_make_text(i, 0, characters[i]))
        else:
            paths = []
            for definition in stroke_datum.paths:
                path = _make_path(definition, path_style)
                paths.append(path)
            g = _make_group(i, 0, paths)
            groups.append(g)
    svg = _make_container(len(stroke_data), 1, groups)
    return svg


def get_steps(word: str) -> str:
    characters = list(word)
    stroke_data = get_stroke_data(characters)
    groups = []
    current_color = _style_stroke_fill('currentColor')
    current_stroke_style = current_color | _opacity('0.9')
    previous_stroke_style = current_color | _opacity('0.7')
    for col, stroke_datum in enumerate(stroke_data):
        if stroke_datum is None:
            groups.append(_make_text(col, 0, characters[col]))
        else:
            for stroke_number, strokes in enumerate(accumulate([d] for d in stroke_datum.paths)):
                paths = []
                for definition in strokes:
                    if definition == strokes[-1]:
                        style = current_stroke_style
                    else:
                        style = previous_stroke_style
                    path = _make_path(definition, style)
                    paths.append(path)
                g = _make_group(col, stroke_number, paths)
                groups.append(g)
    svg = _make_container(len(stroke_data), max(len(s.paths) if s is not None else 1 for s in stroke_data), groups)
    return svg

