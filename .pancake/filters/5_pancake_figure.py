#!/usr/bin/env python

"""
Pandoc filter to convert svg images to pdf transparently as well as allowing margin figure in LaTeX
"""

from utils import *

from pandocfilters import toJSONFilter

def pancake_figure(key, value, format, meta):
    if key == 'Image':
        if format == "latex":
            [[id, classes, properties],name, content] = value
            currentClasses = set(classes)
            image = content[0]
            if 'wide' in currentClasses: 
                if str(image).endswith("svg"):
                    image = tmpPdf(image)
                return [ilatex(latex_command('hypertarget{' + id + '}', '%\n' + begin('figure*') + '\n\\centering\n' + latex_command('includegraphics',image) + '\n' + caption(stringify(name)) + '\n' + end('figure*') + '\n'))]

            if 'margin' in currentClasses: 
                if str(image).endswith("svg"):
                    image = tmpPdf(image)
                return [ilatex(latex_command('marginpar', '%\n' + latex_command('includegraphics',image) + '\n' + captionof(stringify(name)) + label(id) + '\n' ))]

if __name__ == '__main__':
    toJSONFilter(pancake_figure)
