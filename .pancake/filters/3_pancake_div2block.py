#!/usr/bin/env python

"""
Pandoc filter to convert divs with classes specified in configuration to LaTeX blocks of the corresponding environment in LaTeX output.
"""

from utils import *

from pandocfilters import toJSONFilter


def pancake_div2block(key, value, format, meta):
    if key == 'Div':
        if format == "latex":
            [[id, classes, properties], content] = value
            currentClasses = set(classes)
            for _, definedClasses in getMultiMap(meta, 'amsthm').items():
                for definedClass in definedClasses:
                    # Is the classes correct?
                    if definedClass.lower() in currentClasses:
                        return latexblock(properties, definedClass, id, content)
            for definedClass in getSet(meta, 'latexBlocks'):
                if definedClass.lower() in currentClasses:
                    return latexblock(properties, definedClass, id, content)


def latexblock(properties, definedClass, id, content):
    param = ""
    for key_, value in properties:
        if key_ == "param":
            param = value
    name = ""
    for key_, value in properties:
        if key_ == "name":
            name = value
    return [latex(begin(definedClass) + brakets(name) + braces(param) + label(id))] + content + [latex(end(definedClass))]


if __name__ == '__main__':
    toJSONFilter(pancake_div2block)
