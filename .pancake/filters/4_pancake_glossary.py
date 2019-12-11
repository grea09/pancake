#!/usr/bin/env python

"""
Pandoc filter to allow for correct cref usage and more.
"""

from utils import *
import pprint
import sys
import re

from pandocfilters import toJSONFilter

def eprint(x):
    pp = pprint.PrettyPrinter(indent=2, stream=sys.stderr)
    pp.pprint(x)

def gls(x, title, plural, entry):
    command= 'Gls' if title else 'gls'
    if entry:
        command+= 'entry'
        command+= 'name' if (plural) else 'plural'
    else:
        command+= 'pl' if (plural) else ''
    return latex_command(command,x)

def pancake_glossary(key, value, format, meta):
    if format == "latex":
        v = None
        if key == 'Str':
            v = value
        elif key == "Math":
            v = value[1]
        regex = "<([\+-])([^\)]+)>"
        if v is not None and re.search(regex, v) is not None:
            g = []
            s = list(map(raw,re.split(regex, v)))
            for m in re.finditer(regex, v):
                prefix, glsid = m.group(1,2)
                g.append(gls(glsid.lower(), glsid.isupper(), glsid.endswith('s'), prefix == '-'))
            for i,j in enumerate(g):
                s.insert(2*i+1,j)
            print("[DEBUG]", file = sys.stderr)
            eprint(value)
            eprint(s)
            return s

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
