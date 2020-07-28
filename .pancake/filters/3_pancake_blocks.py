#!/usr/bin/env python

"""
Pandoc filter to convert divs with classes specified in configuration to LaTeX blocks of the corresponding environment in LaTeX output.
"""

import logging

from utils import *

from pandocfilters import toJSONFilter


def pancake_div2block(key, value, format, meta):
    if key == 'Div':
        if format == 'latex':
            conf = getMeta(meta, 'elements')
            [[id, classes, properties], content] = value
            for class_ in classes:
                if class_ in allowedClasses(conf):
                    if conf[class_]['theorem']:
                        return theoremblock(properties, class_, id, content)
                    return latexblock(properties, class_, id, content)

def allowedClasses(meta):
    result = []
    for element, dict_ in meta.items():
        if any([k in ['theorem', 'block'] and v 
            for k,v in dict_.items()]):
            result.append(element)
    return set(result)

def theoremblock(properties, definedClass, id, content):
    param = ''
    name = ''
    if 'name' in properties:
        name = properties['name']
    if 'param' in properties:
        param = properties['param']
    if not id:
        id = definedClass + str(hash(stringify(content)))
    return [latex(begin(definedClass) + brakets(param) + '{' + name + '}' + '{' + id + '}')] + content + [latex(end(definedClass))]

def latexblock(properties, definedClass, id, content):
    param = ''
    name = ''
    if 'name' in properties:
        name = properties['name']
    if 'param' in properties:
        param = properties['param']
    return [latex(begin(definedClass) + brakets(name) + braces(param) + label(id))] + content + [latex(end(definedClass))]


if __name__ == '__main__':
    toJSONFilter(pancake_div2block)
