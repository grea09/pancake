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

def getListMap(meta, name):
    # Return a MetaMap as defined in the meta
    #if not hasattr(getListMap, 'value'):
    getListMap.value = {}
    if name in meta and meta[name]['t'] == 'MetaList':
        getListMap.value = []
        for valuemap in meta[name]['c']:
            tmpmap = {}
            if valuemap['t'] == 'MetaMap':
                for key, value in valuemap['c'].items():
                    if value['t'] == 'MetaInlines':
                        string = stringify(value['c'])
                        if re.match('^[a-zA-Z][\w.:-]*$', string):
                            tmpmap[key] = string
            if tmpmap :
                getListMap.value.append(tmpmap)
        getListMap.value = list(getListMap.value)
    return getListMap.value


def getMultiMap(meta, name):
    # Return a MetaMap as defined in the meta
    #if not hasattr(getMultiMap, 'value'):
    getMultiMap.value = {}
    if name in meta and meta[name]['t'] == 'MetaMap':
        for key, values in meta[name]['c'].items():
            if values['t'] == 'MetaList':
                getMultiMap.value[key] = []
                for value in values['c']:
                    string = stringify(value)
                    if re.match('^[a-zA-Z][\w.:-]*$', string):
                        getMultiMap.value[key].append(string)
                getMultiMap.value[key] = set(getMultiMap.value[key])
    return getMultiMap.value

def getMap(meta, name):
    # Return a MetaMap as defined in the meta
    #if not hasattr(getMap, 'value'):
    getMap.value = {}
    if name in meta and meta[name]['t'] == 'MetaMap':
        for key, value in meta[name]['c'].items():
            if value['t'] == 'MetaInlines':
                string = stringify(value['c'])
                if re.match('^[a-zA-Z][\w.:-]*$', string):
                    getMap.value[key] = string
    return getMap.value

def getSet(meta, name):
    # Return a MetaMap as defined in the meta
    #if not hasattr(getSet, 'value'):
    getSet.value = {}
    if name in meta and meta[name]['t'] == 'MetaList':
        getSet.value = []
        for value in meta[name]['c']:
            string = stringify(value)
            if re.match('^[a-zA-Z][\w.:-]*$', string):
                getSet.value.append(string)
        getSet.value = set(getSet.value)
    return getSet.value

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
