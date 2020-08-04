from panflute import run_filter, Div, RawBlock

from utils.latex import block, tcb

def algorithm(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Div:
            conf = doc.get_metadata('elements')
            for class_ in elem.classes:
                if class_ in allowedClasses(conf):
                    if conf[class_]['theorem']:
                        return tcb(elem.attributes, class_, elem.id, elem.content)
                    return block(elem.attributes, class_, elem.id, elem.content)


def allowedClasses(meta):
    result = []
    for element, dict_ in meta.items():
        if any([k in ['theorem', 'block'] and v
                for k, v in dict_.items()]):
            result.append(element)
    return set(result)


def main(doc=None):
    return run_filter(blocks, doc=doc)


if __name__ == "__main__":
    main()
