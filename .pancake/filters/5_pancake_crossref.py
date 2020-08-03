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
            elements = elementsRef(getMeta(meta,'elements'))
            citationid = stuff[0]['citationId']
            title = citationid[0].isupper()
            citationid = citationid.lower()
            if citationid in ['fixme', 'todo', 'citation'] :
                return (ilatex(latex_command('textbf',citationid.upper())))
            prefix = citationid.split(":", 1)[0]
            if prefix in elements:
                element = elements[prefix]
                if 'number' in element and element['number']:
                    return(ilatex(ref(citationid, element['prefix'][0], title)))
                else:
                    return(ilatex(nameref(citationid, element['prefix'][0], title)))
            if ('natbib' in meta and meta['natbib']['c']) or ('biblatex' in meta and meta['biblatex']['c']) :
                return(ilatex(cite(citationid)))

def elementsRef(meta):
    result = {}
    for key, element in meta.items():
        if 'ref' in element:
            result[element['ref']] = element
    return result


if __name__ == '__main__':
    toJSONFilter(pancake_crossref)
