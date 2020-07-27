#!/usr/bin/env python

"""
Pandoc filter to allow for correct cref usage and more.
"""

from utils import *

from pandocfilters import toJSONFilter

def ref(x, name, title):
    return (name.title() if title else name) + "~" + latex_command('ref',x)

def nameref(x, name, title):
    return (name.title() if title else name) + " of " + latex_command('nameref',x)


def pancake_crossref(key, value, format, meta):
    if key == 'Cite':
        if format == "latex":
            [stuff, contents] = value
            citationid = stuff[0]['citationId']
            title = citationid[0].isupper()
            citationid = citationid.lower()
            if citationid in ['before', 'later', 'citation'] :
                return (ilatex(latex_command('textbf',citationid.upper())))
            prefix = citationid.split(":", 1)[0]
            for env in getMeta(meta,'ref-numbered') :
              if prefix == getKey(env) :
                return(ilatex(ref(citationid, getValue(env), title)))
            for env in getMeta(meta,'ref-named') :
              if prefix == getKey(env) :
                return(ilatex(nameref(citationid, getValue(env), title)))
            if ('natbib' in meta and meta['natbib']['c']) or ('biblatex' in meta and meta['biblatex']['c']) :
                return(ilatex(cite(citationid)))

if __name__ == '__main__':
    toJSONFilter(pancake_crossref)
