from panflute import run_filter, Image, RawInline

from utils.file import convert2pdf
from utils.latex import begin, caption, captionof,  label, image, latex_command, end


def figure(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Image and set(elem.classes).intersection({'wide', 'margin'}):
            if elem.url.endswith('svg'):
                    f = convert2pdf(elem.url)
            if 'wide' in elem.classes:
                return RawInline(latex_command('hypertarget{' + elem.identifier + '}',
                                                         '%\n' + begin('figure*') + '\n\\centering\n' +
                                                         image(f) + '\n' +
                                                         caption(elem.title) + '\n' +
                                                         end('figure*') + '\n'), 'latex')

            if 'margin' in elem.classes:
                return RawInline(latex_command('marginpar', '%\n' +
                                                         image(elem.url) + '\n' +
                                                         captionof(elem.title) + label(elem.id) + '\n'), 'latex')


def main(doc=None):
    return run_filter(figure, doc=doc)

if __name__ == "__main__":
    main()
