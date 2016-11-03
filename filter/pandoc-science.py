#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="algorithm" to LaTeX
algorithm environments in LaTeX output, and to numbered algorithm
in HTML output.
"""
from __future__ import print_function
import sys
import re

from pandocfilters import toJSONFilter, stringify, RawBlock, Div, RawInline, Str

def warning(*objs):
    print("[WARNING] ", *objs, file=sys.stderr)

def debug(*objs):
     print("[DEBUG] ", *objs, file=sys.stderr)

def latex(x):
    return RawBlock('tex', x)

def ilatex(x):
     return RawInline('tex', x)


def html(x):
    return RawBlock('html', x)

def latex_command(name, content):
    if content == "":
        return ""
    else:
        return '\\' + name + '{' + content + '}'

def caption(x):
    return latex_command('caption',x)

def label(x):
    return latex_command('label',x)

def ref(x, title):
    return latex_command('Cref' if title else 'cref',x)


def begin(x):
    return latex_command('begin',x)
def end(x):
    return latex_command('end',x)


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

def getMultiMap(meta, name):
    # Return a MetaMap as defined in the meta
    if not hasattr(getMultiMap, 'value'):
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
    if not hasattr(getMap, 'value'):
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
    if not hasattr(getSet, 'value'):
        getSet.value = {}
        if name in meta and meta[name]['t'] == 'MetaList':
            getSet.value = []
            for value in meta[name]['c']:
                string = stringify(value)
                if re.match('^[a-zA-Z][\w.:-]*$', string):
                    getSet.value.append(string)
            getSet.value = set(getSet.value)
    return getSet.value


def pandoc_science(key, value, format, meta):
    if key == 'Div':
       # Get the attributes
        [[id, classes, properties], content] = value

        currentClasses = set(classes)

        for environment, definedClasses in getMultiMap(meta, 'amsthm').items():
            for definedClass in definedClasses:
                # Is the classes correct?
                if definedClass.lower() in currentClasses:
                    if format == "latex":
                        key_ = ""
                        if len(properties) > 0:
                            [[key_, value]] = properties
                        if key_ == "name":
                            name = value
                        else:
                            name = ""
                        return [latex(begin(definedClass) + brakets(name) + label(id))] + content + [latex(end(definedClass))]
                    break
    elif key == 'Cite':
        [stuff, contents] = value
        citationid = stuff[0]['citationId']
        title = citationid[0].isupper()
        citationid = citationid.lower()
        _prefix = citationid.split(":", 1)[0]
        for prefix in getSet(meta, 'amsthmPrefixes'):
            if _prefix == prefix:
                if format == "latex":
                    return(ilatex(ref(citationid, title)))

if __name__ == '__main__':
    toJSONFilter(pandoc_science)

