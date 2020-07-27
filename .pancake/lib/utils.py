#!/usr/bin/env python

"""
Library for makinf Pandoc filters for LaTeX easier
"""

import os
import re
import tempfile

from pandocfilters import stringify, RawBlock, RawInline, walk

def tmpPdf(svg):
    pdf = tempfile.NamedTemporaryFile(delete=True)
    os.system('rsvg-convert -f pdf -a -o ' + pdf.name + '.pdf ' + svg)
    return pdf.name

def latex(x):
    return RawBlock('tex', x)

def ilatex(x):
     return RawInline('tex', x)

def html(x):
    return RawBlock('html', x)

def latex_command(name, content, **kwargs):
    if content == "":
        return ""
    else:
        return '\\' + name + (('[' + kwargs.get('option') + ']') if 'option' in kwargs else '') + '{' + content + '}'

def caption(x):
    return latex_command('caption',x)

def captionof(x):
    return latex_command('captionof{figure}',x)

def label(x, *args, **kwargs):
    if len(args) >= 1:
        return latex_command('label',x, option=args[0])
    else:
        return latex_command('label',x)

def begin(x):
    return latex_command('begin',x)
def end(x):
    return latex_command('end',x)


def braces(x):
    if x == "":
        return ""
    else:
        return '{' + x + '}'

def brakets(x):
    if x == "":
        return ""
    else:
        return '[' + x + ']'

def parentesis(x):
    if x == "":
        return ""
    else:
        return '(' + x + ')'


def getMeta(meta, key):
    # Return a structured data from a key
    # as defined in the meta
    if key in meta :
        return decodeMeta(meta[key])

def decodeMeta(meta):
    # Return a structured data as defined in the meta
    #if not hasattr(getMap, 'value'):
    decode = {
        'MetaBool': bool,
        'MetaInlines': stringify,
        'MetaList': decodeList,
        'MetaMap': decodeMap,
    }
    return decode[meta['t']](meta['c'])

def decodeList(metaList):
    # Return a list as encoded in the meta
    result = []
    for value in metaList:
        result.append(decodeMeta(value))
    return result  

def decodeMap(metaMap):
    # Return a dict as encoded in the meta
    result = {}
    for key, value in metaMap.items():
        result[key] = decodeMeta(value)
    return result

def getKey(dictionary):
    key, value = next(iter(dictionary.items()))
    return key

def getValue(dictionary):
    key, value = next(iter(dictionary.items()))
    return value

def raw(x):
    result = []
    def flatten(key, val, format, meta):
        if val is not None :
            if isinstance(val[1], unicode) :
                result.append(val[1])
            if isinstance(val[1], dict) :
                result.append(" ")
    walk(x, flatten, "", {})
    return ''.join(result)
