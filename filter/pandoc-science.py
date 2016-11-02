#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="algorithm" to LaTeX
algorithm environments in LaTeX output, and to numbered algorithm
in HTML output.
"""
from __future__ import print_function
import sys

from pandocfilters import toJSONFilter, RawBlock, Div, RawInline, Str

counts = {'algorithm': 0, 'proof' : 0, 'definition' : 0, 'lemma' : 0}
refs = {'algorithm': {}, 'proof' : {}, 'definition' : {}, 'lemma' : {}}

def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

def latex(x):
    return RawBlock('latex', x)

def ilatex(x):
     return RawInline('latex', x)


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


def algorithm(name, label, content):
    return([latex('\\begin{algorithm}' + caption(name) + label + '\\begin{algorithmic}[1]')] + content + [latex('\\end{algorithmic}\\end{algorithm}')])

def proof(name, label, content):
    return([latex('\\begin{proof}' + brakets(name) + label)] + content + [latex('\\end{proof}')])

def definition(name, label, content):
    return([latex('\\begin{definition}' + brakets(name) + label)] + content + [latex('\\end{definition}')])

def lemma(name, label, content):
    return([latex('\\begin{lemma}' + brakets(name) + label)] + content + [latex('\\end{lemma}')])


def pandoc_science(key, value, format, meta):
    global refs, counts
    names = {'algorithm': 'Algorithm', 'proof' : 'Proof', 'definition' : 'Definition', 'lemma' : 'Lemma'}
    prefixes = {'alg': 'algorithm', 'prf' : 'proof', 'def' : 'definition', 'lem' : 'lemma'}
    formats = {'algorithm': algorithm, 'proof' : proof, 'definition' : definition, 'lemma' : lemma}
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        for class_ in classes:
            if class_ in refs:
                counts[class_] = counts[class_]+1
                refs[class_].update({ident : counts[class_]})
                key_ = ""
                if len(kvs) > 0:
                    [[key_, value]] = kvs
                if key_ == "name":
                    name = value
                else:
                    name = ""
                
                if format == "latex":
                    return formats[class_](name, label(ident), contents)
                elif format == "html" or format == "html5":
                    newcontents = [html('<dt>' + names[class_] + ' ' + str(len(refs[class_])) + '</dt>'),
                                   html('<dd>')] + contents + [html('</dd>\n</dl>')]
                    return Div([ident, classes, kvs], newcontents)
                else:
                    return Div([ident, classes, kvs], [ html('<dt>' + names[class_] + ' ' + str(counts[class_]) + '</dt> ' + parentesis(name)) ] + contents)
    elif key == 'Span':
        [[ident, classes, kvs], contents] = value
        for class_ in classes:
            if class_ == 'proc':
                if format == "latex":
                    return([ilatex('\\textproc{')] + contents + [ilatex('}')])
    elif key == 'Cite':
        [stuff, contents] = value
        citationid = stuff[0]['citationId']
        title = citationid[0].isupper()
        citationid = citationid.lower()
        prefix = citationid.split(":", 1)[0]
        if prefix in prefixes:
            class_ = prefixes[prefix]
            name = names[class_].lower()
            if title:
                name = name.title()
            if format == "latex":
                return(RawInline('latex', '\\cref{' + citationid + '}'))
            else:
                return Str(name + ' ' + str(refs[class_].get(citationid, '??' )))
        elif prefix == 'line':
            name = 'line'
            if title:
                name = name.title()
            return(RawInline('latex', '\\cref{' + citationid + '}'))

if __name__ == "__main__":
    toJSONFilter(pandoc_science)
