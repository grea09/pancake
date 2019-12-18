#!/usr/bin/env python

"""
Pandoc filter to allow for correct cref usage and more.
"""

from utils import *
import re

from pandocfilters import toJSONFilter

def gls(entry, glsid):
    command= 'Gls' if glsid.isupper() else 'gls'
    if entry == '-':
        command+= 'entry'
        command+= 'name' if (glsid.endswith('S')) else 'plural'
    elif entry == '+':
        command+= 'pl' if (glsid.endswith('S')) else ''
    return ilatex(latex_command(command,glsid.lower()))

def pancake_glossary(key, value, format, meta):
    if format == "latex":
        regex = "<([\+-])([^!\)]+)>"
        if key == 'Str':
            if re.search(regex, value) is not None:
                return gls(*re.match(regex, value).group(1,2))

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
