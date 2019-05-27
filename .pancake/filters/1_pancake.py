#!/usr/bin/env python

"""
Pandoc filter to convert divs with classes specified in configuration to LaTeX
theorem environments in LaTeX output, and to numbered theorems
in HTML output.
"""

from __future__ import print_function

import sys
import os
import re
import pprint
import tempfile

from pprint import pprint

from pandocfilters import toJSONFilter, stringify, RawBlock, Div, RawInline, Str, walk

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

def cite(x):
    return latex_command('cite',x)

def caption(x):
    return latex_command('caption',x)

def captionof(x):
    return latex_command('captionof{figure}',x)

def label(x, t):
    return latex_command('label',x, option=t)

def ref(x, name, title):
#    return (name.title() if title else name) + " " + latex_command('ref',x)
    return latex_command('cref',x)

def labelref(x, title):
    return latex_command('nameCref' if title else 'namecref',x) + ' of ' + latex_command('nameref',x)

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

def raw(x):
    result = []
    def flatten(key, val, format, meta):
        if val is not None :
            if isinstance(val[1], unicode) :
#                pprint.pprint(val[1], sys.stderr)
                result.append(val[1])
            if isinstance(val[1], dict) :
#                pprint.pprint(val, sys.stderr)
                result.append(" ")
    walk(x, flatten, "", {})
    return ''.join(result)

def pandoc_science(key, value, format, meta):
    if key == 'Div':
        if format == "latex":
            [[id, classes, properties], content] = value
            currentClasses = set(classes)
            for environment, definedClasses in getMultiMap(meta, 'amsthm').items():
                for definedClass in definedClasses:
                    # Is the classes correct?
                    if definedClass.lower() in currentClasses:
                        param = ""
                        for key_, value in properties:
                            if key_ == "param":
                                param = value
                        name = ""
                        for key_, value in properties:
                            if key_ == "name":
                                name = value
                        return [latex(begin(definedClass) + brakets(name) + braces(param) + label(id,definedClass))] + content + [latex(end(definedClass))]
                        break
            for definedClass in getSet(meta, 'latexBlocks'):
                # Is the classes correct?
                #pprint(currentClasses, stream=sys.stderr)
                if definedClass.lower() in currentClasses:
                    param = ""
                    for key_, value in properties:
                        if key_ == "param":
                            param = value
                    name = ""
                    for key_, value in properties:
                        if key_ == "name":
                            name = value
                    return [latex(begin(definedClass) + brakets(name) + braces(param) + label(id,definedClass))] + content + [latex(end(definedClass))]
                    break
    elif key == 'CodeBlock':
        if format == "latex":
            [[id, classes, properties], content] = value
            currentClasses = set(classes)
            if meta['algorithm'] is None:
                definedClass = "algorithm"
            else:
                definedClass = stringify(meta['algorithm']['c']).lower()
            if definedClass in currentClasses:
                name = ""
                numbered = ""
                for key_, value in properties:
                    if key_ == "name":
                        name = value
                    elif key_ == "startLine":
                        numbered = "[" + value + "]"
                return [latex(begin(definedClass) + caption(name) + label(id,definedClass) + begin("algorithmic") + numbered + content + end("algorithmic") + end(definedClass))]
    elif key == 'Cite':
        if format == "latex":
            [stuff, contents] = value
            citationid = stuff[0]['citationId']
            title = citationid[0].isupper()
            citationid = citationid.lower()
            if citationid in ['before', 'later', 'citation'] :
                return (ilatex(latex_command('textbf',citationid.upper())))
            prefix = citationid.split(":", 1)[0]
            numbered = getListMap(meta,'cref-numbered')
            for env in numbered :
              if prefix == env['prefix'] :
                return(ilatex(ref(citationid, env['name'], title)))
            if prefix in [d['prefix'] for d in getListMap(meta,'cref-labelled')] :
                return(ilatex(labelref(citationid, title)))
            if ('natbib' in meta and meta['natbib']['c']) or ('biblatex' in meta and meta['biblatex']['c']) :
                return(ilatex(cite(citationid)))
    elif key == 'Image':
        if format == "latex":
            [[id, classes, properties],name, content] = value
            currentClasses = set(classes)
            image = content[0]
            if 'wide' in currentClasses: 
                if str(image).endswith("svg"):
                    image = tmpPdf(image)
                return [ilatex(latex_command('hypertarget{' + id + '}', '%\n' + begin('figure*') + '\n\\centering\n' + latex_command('includegraphics',image) + '\n' + caption(stringify(name)) + label(id,'figure') + '\n' + end('figure*') + '\n'))]

            if 'margin' in currentClasses: 
                if str(image).endswith("svg"):
                    image = tmpPdf(image)
                return [ilatex(latex_command('marginpar', '%\n' + latex_command('includegraphics',image) + '\n' + captionof(stringify(name)) + label(id,'figure') + '\n' ))]

if __name__ == '__main__':
    toJSONFilter(pandoc_science)

