#!/usr/bin/env python

"""
Pandoc filter to allow for correct cref usage and more.
"""

from utils import *
import re

from pandocfilters import toJSONFilter

def gls(x, title, plural, entry):
    command= 'Gls' if title else 'gls'
    if entry:
        command+= 'entry'
        command+= 'name' if (plural) else 'plural'
    else:
        command+= 'pl' if (plural) else ''
    return latex_command(command,x)


def pancake_glossary(key, value, format, meta):
    if key == 'Str':
        if format == "latex":
            print(value)
            #prefix, id = re.match("\(([+-])([^\)]+)\)")

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
