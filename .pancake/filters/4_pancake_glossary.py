#!/usr/bin/env python

"""
Pandoc filter to add glossary capabilities
"""

from utils import *
from itertools import chain, zip_longest
import re

from pandocfilters import toJSONFilter, Str

def gls(entry, glsid):
    command= 'Gls' if glsid.isupper() else 'gls'
    if entry == '-':
        command+= 'entry'
        command+= 'name' if (glsid.endswith('S')) else 'plural'
    elif entry == '+':
        command+= 'pl' if (glsid.endswith('S')) else ''
    glsid = glsid.lower()[:-1] if (glsid.endswith('S')) else glsid.lower()
    return ilatex(latex_command(command,glsid))

def pancake_glossary(key, value, format, meta):
    if format == "latex":
        r = re.compile(r"<([\+-])([^!>]+)>")
        if key == 'Str':
            if r.search(value) is not None:
                keep = lambda x: ((x['c'] != '') and (r.match(str(x['c'])) == None))
                parse = lambda m: gls(*m.group(1,2))
                result = list(filter(keep, 
                    chain.from_iterable(
                      zip_longest(
                        map(Str, re.split(r"<[\+-][^!>]+>", value)), 
                        map(parse, r.finditer(value)), fillvalue=Str('')))))
                return result

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
