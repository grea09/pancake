from panflute import run_filter, CodeBlock, RawBlock
import logging

from utils.latex import begin, caption, label, end

algEnv = 'algorithm'


def code(elem, doc):
    if doc.format == 'latex':
        if type(elem) == CodeBlock:
            if algEnv in elem.classes:
                name = ''
                numbered = "[1]"
                if 'name' in elem.attributes:
                    name = elem.attributes['name']
                if 'startLine' in elem.attributes:
                    numbered = '[' + elem.attributes['startLine'] + ']'
                return RawBlock(begin(algEnv) +
                                caption(name) + label(elem.identifier) +
                                begin('algorithmic') + numbered + elem.text +
                                end('algorithmic') + end(algEnv), 'latex')
            languages = set(doc.get_metadata('listings-langages').keys()).intersection(elem.classes)
            if languages :
                elem.attributes['language'] = languages.pop()
                return elem


def main(doc=None):
    return run_filter(code, doc=doc)


if __name__ == "__main__":
    main()
