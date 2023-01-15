import json
import mmap

from importlib.resources import files
from typing import NamedTuple


class StrokeData(NamedTuple):
    r'''The description of strokes within a character.
    
    :ivar character: The character to which these stroke data pertain
    :ivar paths: each stroke's shape as an SVG path definition string
    :ivar medians: for each stroke, a list of coordinates of its turning points
    '''
    character: str
    paths: list[str]
    medians: list[list[tuple[int, int]]]


def _convert_graphics(entry: dict) -> StrokeData:
    character = entry['character']
    paths = entry['strokes']
    medians = [[tuple(median) for median in medians] for medians in entry['medians']]
    return StrokeData(character, paths, medians)


def get_stroke_data(characters: list[str]) -> list[StrokeData]:
    results = [None] * len(characters)
    ch_index = len('{"character":"') # the index in each line where the character for that entry is
    data_module = '.'.join(__name__.split('.')[:-1] + ['data'])
    with files(data_module).joinpath('graphics.txt').open(encoding='utf-8') as graphics:
        for line in graphics:
            if line[ch_index] in characters:
                entry = json.loads(line)
                stroke_data = _convert_graphics(entry)
                results[characters.index(line[ch_index])] = stroke_data
    return results

