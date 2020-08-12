from panflute import run_filter, Cite, Citation, Space, Str, RawInline, Para

from utils.latex import latex_command


def prefixes(meta):
    result = {}
    for _, element in meta.items():
        if 'ref' in element:
            result[element['ref']] = element
    return result


def render(meta, citations, conjunction):
    if len(citations) == 0:
        return
    result = ''
    prefix = meta['prefix']
    command = 'ref' if 'number' in meta else 'nameref'
    if len(citations) > 1 :
        prefix = prefix[1] # Plurial
    else:
        prefix = prefix[0] # Singular
    if citations[0].id[0].isupper(): # Title case
        prefix = prefix.title()
    else:
        prefix = prefix.lower()
    result += prefix + '~'
    if 'preposition' in meta and 'number' not in meta:
        result += meta['preposition'] + '~'
    result += latex_command(command, citations[0].id.lower())
    for citation in citations[1:-1]:
        result += ', ' + latex_command(command, citation.id.lower())
    if len(citations) > 1:
        result += ' ' + conjunction + ' '
        result += latex_command(command, citations[-1].id.lower())
    return result
    
    


def crossref(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Cite:
            metaPrefix = prefixes(doc.get_metadata('elements'))
            citations = {}
            for citation in elem.citations :
                split = citation.id.split(":", 1)
                ref = split[0].lower()
                if len(split) <= 1 or ref not in metaPrefix:
                    return
                if ref not in citations:
                    citations[ref] = []
                citations[ref].append(citation)
            result = ''
            for ref, prefixed in citations.items() :
                result += render(metaPrefix[ref], prefixed, doc.get_metadata('ref-conjunction'))
            return RawInline(result, 'latex')

            


def main(doc=None):
    return run_filter(crossref, doc=doc)


if __name__ == "__main__":
    main()
