from panflute import run_filter, Cite, Citation, Space, Str, RawInline

from utils.latex import latex_command


def prefixes(meta):
    result = {}
    for key, element in meta.items():
        if 'ref' in element:
            result[element['ref']] = element
    return result


def render(meta, citations, conjunction):
    result = []
    prefix = meta['prefix']
    command = 'ref' if 'number' not in meta else 'nameref'
    if len(citations) > 1 :
        prefix = prefix[1] # Plurial
    else:
        prefix = prefix[0] # Singular
    if citations[0].id[0].isupper(): # Title case
        prefix = prefix.title()
    else:
        prefix = prefix.lower()
    result.append(Str(prefix))
    if 'preposition' in meta and 'number' not in meta:
        result.append(Space())
        result.append(Str(meta['preposition']))
    for citation in citations[:-1]:
        result.append(RawInline('latex', latex_command(command, citation.id)))
        result.append([Str(','), Space()])
    result.append([Space(), Str(conjunction), Space()])
    result.append(RawInline('latex', latex_command(command, citations[-1].id)))
    return result
    
    


def crossref(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Cite:
            prefixes = prefixes(doc.get_metadata('elements'))
            citations = {}
            for citation in elem.citations :
                prefix = citation.id.split(":", 1)[0]
                if prefix not in citations:
                    citations[prefix] = []
                citation[prefix].append(citation)
            for prefix, prefixed in citation.items() :
                render(prefixes[prefix], prefixed, doc.get_metadata('ref-conjunction'))

            


def main(doc=None):
    return run_filter(crossref, doc=doc)


if __name__ == "__main__":
    main()
