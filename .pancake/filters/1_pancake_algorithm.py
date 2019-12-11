#!/usr/bin/env python

"""
Pandoc filter to convert code blocks with classes specified in configuration to LaTeX algorithm environments in LaTeX output.
"""

from utils import *

from pandocfilters import toJSONFilter

def pancake_algorithm(key, value, format, meta):
    if key == 'CodeBlock':
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
                return [latex(begin(definedClass) + caption(name) + label(id) + begin("algorithmic") + numbered + content + end("algorithmic") + end(definedClass))]

if __name__ == '__main__':
    toJSONFilter(pancake_algorithm)
