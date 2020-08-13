from panflute import run_filter, Div, RawBlock, CodeBlock

from utils.latex import begin, end, braces, brakets, label, caption

def blocks(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Div:
            conf = doc.get_metadata('elements')
            for class_ in elem.classes:
                if class_ in allowedClasses(conf):
                    if conf[class_]['theorem']:
                        return tcb(elem, class_, 'number' in conf[class_])
                    return block(elem, class_)
        if type(elem) == CodeBlock:
            conf = doc.get_metadata('elements')
            for class_ in elem.classes:
                if class_ in allowedClasses(conf):
                    if conf[class_]['listing']:
                        listing = tcb(elem, class_, 'number' in conf[class_])
                        listing[1] = RawBlock(elem.text, 'latex')
                        return listing


def tcb(elem, definedClass, numbered):
    param = ''
    name = ''
    additional = '{}'
    if 'name' in elem.attributes:
        name = elem.attributes['name']
        param = 'nameref=' + braces(name) +','
    if 'caption' in elem.attributes:
        param = 'caption=' + braces(elem.attributes['caption']) +','
    if 'param' in elem.attributes:
        param = elem.attributes['param']
    if elem.identifier:
        param = 'label=' + braces(elem.identifier) + ',' + param
    if not numbered:
        definedClass += '*'
    else:
        additional = '{' + elem.identifier + '}'
    beginElem = RawBlock(begin(definedClass) + brakets(param) + '{' + name + '}' + additional, 'latex')
    endElem = RawBlock(end(definedClass), 'latex')
    return [beginElem, elem, endElem]


def block(elem, definedClass):
    param = ''
    name = ''
    if 'name' in elem.attributes:
        name = elem.attributes['name']
    if 'param' in elem.attributes:
        param = elem.attributes['param']
    beginElem = RawBlock(begin(definedClass) + brakets(name) + braces(param) + label(elem.identifier), 'latex')
    endElem = RawBlock(end(definedClass), 'latex')
    return [beginElem, elem, endElem]


def allowedClasses(meta):
    result = []
    for element, dict_ in meta.items():
        if any([k in ['theorem', 'block', 'listing'] and v
                for k, v in dict_.items()]):
            result.append(element)
    return set(result)


def main(doc=None):
    return run_filter(blocks, doc=doc)


if __name__ == "__main__":
    main()
