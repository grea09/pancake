#!/usr/bin/env python

"""
Pandoc filter to convert divs with classes specified in configuration to LaTeX
theorem environments in LaTeX output, and to numbered theorems
in HTML output.
"""

from __future__ import print_function

import sys
import re
import pprint

from pandocfilters import toJSONFilter, stringify, RawBlock, Div, RawInline, Str, walk

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

def raw(x):
    result = []
    def flatten(key, val, format, meta):
        if val is not None :
            if isinstance(val[1], unicode) :
                pprint.pprint(val[1], sys.stderr)
                result.append(val[1])
            if isinstance(val[1], dict) :
                pprint.pprint(val, sys.stderr)
                result.append(" ")
    walk(x, flatten, "", {})
    return ''.join(result)


def pandoc_science(key, value, format, meta):
    if key == 'Div':
        [[id, classes, properties], content] = value
        currentClasses = set(classes)
        for environment, definedClasses in getMultiMap(meta, 'amsthm').items():
            for definedClass in definedClasses:
                # Is the classes correct?
                if definedClass.lower() in currentClasses:
                    if format == "latex":
                        name = ""
                        for key_, value in properties:
                            if key_ == "name":
                                name = value
                        return [latex(begin(definedClass) + brakets(name) + label(id))] + content + [latex(end(definedClass))]
                    break
        for definedClass in getSet(meta, 'latexBlocks'):
            # Is the classes correct?
            if definedClass.lower() in currentClasses:
                if format == "latex":
                    name = ""
                    for key_, value in properties:
                        if key_ == "name":
                            name = value
                    return [latex(begin(definedClass) + brakets(name) + label(id))] + content + [latex(end(definedClass))]
                break
    elif key == 'CodeBlock':
        [[id, classes, properties], content] = value
        currentClasses = set(classes)
        definedClass = stringify(meta['pseudocode']['c']).lower()
        if definedClass in currentClasses:
            if format == "latex":
                name = ""
                numbered = ""
                for key_, value in properties:
                    if key_ == "name":
                        name = value
                    elif key_ == "startLine":
                        numbered = "[" + value + "]"
                return [latex(begin(definedClass) + caption(name) + label(id) + begin("algorithmic") + numbered + content + end("algorithmic") + end(definedClass))]
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
    elif key == 'Image':
        if format == "latex":
            [[id, classes, properties],name, content] = value
            currentClasses = set(classes)
            if 'wide' in currentClasses: 
                #TODO add rsvg-convert ["-f","pdf","-a","-o",pdfOut,fname] + tempfile.NamedTemporaryFile(
                return [ilatex(latex_command('hypertarget{' + id + '}', '%\n' + begin('figure*') + '\n\\centering\n' + latex_command('includegraphics',content[0]) + '\n' + caption(stringify(name)) + label(id) + '\n' + end('figure*') + '\n'))]

if __name__ == '__main__':
    toJSONFilter(pandoc_science)

