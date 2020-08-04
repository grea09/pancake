import os
import tempfile

def convert2pdf(svg):
    pdf = tempfile.NamedTemporaryFile(delete=True)
    os.system('rsvg-convert -f pdf -a -o ' + pdf.name + '.pdf ' + svg)
    return pdf.name