#!/usr/bin/env python

"""
Pandoc filter to convert code blocks with classes specified in configuration to LaTeX algorithm environments in LaTeX output.
"""

from utils import *

from pandocfilters import toJSONFilter

algEnv = "algorithm"

def pancake_algorithm(key, value, format, meta):
    if key == 'CodeBlock':
        if format == "latex":
            [[id, classes, properties], content] = value
            currentClasses = set(classes)
            if algEnv in currentClasses:
                name = ""
                numbered = "[1]"
                for key_, value in properties:
                    if key_ == "name":
                        name = value
                    elif key_ == "startLine":
                        numbered = "[" + value + "]"
                return [latex(begin(algEnv) + caption(name) + label(id) + begin("algorithmic") + numbered + content + end("algorithmic") + end(algEnv))]

if __name__ == '__main__':
    toJSONFilter(pancake_algorithm)
