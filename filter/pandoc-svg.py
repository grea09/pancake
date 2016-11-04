#! /usr/bin/env python
"""
Pandoc filter to convert svg files to pdf as suggested at:
https://github.com/jgm/pandoc/issues/265#issuecomment-27317316
"""

__author__ = "Jerome Robert"

import mimetypes
import subprocess
import os
import sys
from pandocfilters import toJSONFilter, Image

# TODO add emf export if fmt=="docx" ?
fmt_to_option = {
    "latex": ("--export-pdf", "pdf"),
    "beamer": ("--export-pdf", "pdf"),
    # because of IE
    "html": ("--export-png", "png")
}


def svg_to_any(key, value, fmt, meta):
    if key == 'Image':
        alt, [src, title] = value[1], value[-1]
        mimet, _ = mimetypes.guess_type(src)
        option = fmt_to_option.get(fmt)
        if mimet == 'image/svg+xml' and option:
            base_name, _ = os.path.splitext(src)
            eps_name = base_name + "." + option[1]
            try:
                mtime = os.path.getmtime(eps_name)
            except OSError:
                mtime = -1
            if mtime < os.path.getmtime(src):
                cmd_line = ['inkscape', '-z', option[0] , eps_name, src]
                #sys.stderr.write("Running %s\n" % " ".join(cmd_line))
                ps = subprocess.Popen(cmd_line, stderr=subprocess.PIPE)
                error = subprocess.check_output(('grep', '-v', 'Gtk'), stdin=ps.stderr)
                ps.wait()
                print >> sys.stderr, error
            return Image(value[0], alt, [eps_name, title])

if __name__ == "__main__":
    toJSONFilter(svg_to_any)
