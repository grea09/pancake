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

def gls(prefix, glsid):
    command= 'Gls' if glsid.isupper() else 'gls'
    if prefix == '-':
        command+= 'entry'
        command+= 'name' if (glsid.endswith('S')) else 'plural'
    else:
        command+= 'pl' if (glsid.endswith('S')) else ''
    return ilatex(latex_command(command,glsid.lower()))

def pancake_glossary(key, value, format, meta):
    if format == "latex":
        regex = "<([\+-])([^\)]+)>"
        if key == 'Str':
            if re.search(regex, value) is not None:
                return gls(*re.match(regex, value).group(1,2))
        elif key == "Math":
            v = value[1]
            if v is not None and re.search(regex, v) is not None:
                g = []
                s = list(map(Str,re.split(regex, v)))
                for m in re.finditer(regex, v):
                    g.append(gls(*m.group(1,2)))
                for i,j in enumerate(g):
                    s.insert(2*i+1,j)
                # print("[DEBUG]", file = sys.stderr)
                # eprint(value)
                # eprint(s)
                return s

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
