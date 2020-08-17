from panflute import run_filter, Image, RawInline, Div, RawBlock, Para, Str, Space

from utils.file import convert2pdf
from utils.latex import begin, caption, captionof,  label, image, latex_command, end


def figure(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Image and set(elem.classes).intersection({'wide', 'margin', 'subfigure'}):
            params = elem.attributes
            if 'name' in params:
                del params['name']
            if 'caption' in params:
                del params['caption']
            if elem.url.endswith('svg'):
                f = convert2pdf(elem.url)
                elem.url = str(f)
            if 'width' in elem.attributes:
                width = elem.attributes['width']
                if width.endswith('%'):
                    width = str(float(width.strip('%'))/100.0) + '\\textwidth'
                params['width'] = width
            if not elem.title:
                elem.title = ''
                for e in elem.content:
                    if type(e) == Str:
                        elem.title += e.text
                    if type(e) == Space:
                        elem.title += ' '
            if 'wide' in elem.classes:
                return RawInline(latex_command('hypertarget{' + elem.identifier + '}',
                                               '%\n' + begin('figure*') + '\n\\centering\n' +
                                               image(elem.url, **params) + '\n' +
                                               caption(elem.title) + '\n' +
                                               end('figure*') + '\n'), 'latex')
            if 'subfigure' in elem.classes:
                return RawInline(latex_command('subfloat',
                                               image(elem.url, **params) + '\n' +
                                               label(elem.identifier), option=elem.title), 'latex')
            if 'margin' in elem.classes:
                return RawInline(latex_command('marginpar', '%\n' +
                                               image(elem.url, **params) + '\n' +
                                               captionof(elem.title) + label(elem.identifier) + '\n'), 'latex')
        if type(elem) == Div and 'figure' in elem.classes:
            result = begin('figure') + '[h]' + begin('center')
            for e in elem.content:
                if type(e) == Para:
                    for _e in e.content:
                        if type(_e) == Image:
                            _e.classes.append('subfigure')
                            result += figure(_e, doc).text
                    continue
                if type(_e) == Image:
                    e.classes.append('subfigure')
                    result += figure(e, doc).text
            if 'caption' in elem.attributes:
                result += captionof(elem.attributes['caption'])
            result += label(elem.identifier) + end('center') + end('figure')
            elem.content.clear()
            elem.content.insert(0, RawBlock(result, 'latex'))


def main(doc=None):
    return run_filter(figure, doc=doc)


if __name__ == "__main__":
    main()
