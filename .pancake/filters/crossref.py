import logging

from panflute import run_filter, Cite, Citation, Space, Str, RawInline, Para

from utils.latex import latex_command


def prefixes(meta):
    result = {}
    for _, element in meta.items():
        if 'ref' in element:
            result[element['ref']] = element
    return result


def render(meta, citations, conjunction):
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
    for citation in citations[:-1]:
        result += latex_command(command, citation.id) + ', '
    if len(citations) > 1:
        result += ' ' + conjunction + ' '
    result += latex_command(command, citations[-1].id)
    return result
    
    


def crossref(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Cite:
            metaPrefix = prefixes(doc.get_metadata('elements'))
            citations = {}
            for citation in elem.citations :
                split = citation.id.split(":", 1)
                logging.warning("split=%s", split)
                if len(split) <= 1 or split[0] not in metaPrefix:
                    continue
                prefix = split[0]
                if prefix not in citations:
                    citations[prefix] = []
                citations[prefix].append(citation)
            result = ''
            for prefix, prefixed in citations.items() :
                result += render(metaPrefix[prefix], prefixed, doc.get_metadata('ref-conjunction'))
            logging.warning("render=%s", result)
            return RawInline(result, 'latex')

            


def main(doc=None):
    return run_filter(crossref, doc=doc)


if __name__ == "__main__":
    main()
