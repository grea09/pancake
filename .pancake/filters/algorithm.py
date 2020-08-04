from panflute import run_filter, CodeBlock, RawBlock

from utils.latex import begin, caption, label, end

algEnv = 'algorithm'


def algorithm(elem, doc):
    if doc.format == 'latex':
        if type(elem) == CodeBlock:
            if algEnv in elem.classes:
                name = ''
                numbered = "[1]"
                if 'name' in elem.attributes.items():
                    name = elem.attributes['name']
                if 'name' in elem.attributes.items():
                    numbered = '[' + elem.attributes['name'] + ']'
                return RawBlock('latex', begin(algEnv) +
                                caption(name) + label(elem.id) +
                                begin('algorithmic') + numbered + elem.content +
                                end('algorithmic') + end(algEnv))


def main(doc=None):
    return run_filter(algorithm, doc=doc)


if __name__ == "__main__":
    main()
