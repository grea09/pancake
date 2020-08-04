from panflute import run_filter, Str, RawInline
from itertools import chain, zip_longest
import re

from utils.latex import gls

r = re.compile(r"<([\+-])([^!>]+)>")


def glossary(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Str:
            if r.search(elem.text) is not None:
                def keep(x): return ((x['c'] != '') and (
                    r.match(str(x['c'])) == None))

                def parse(m): return RawInline('latex', gls(*m.group(1, 2)))
                result = list(filter(keep,
                                     chain.from_iterable(
                                         zip_longest(
                                             map(Str, r.split(
                                                 elem.text) + [' ']),
                                             map(parse, r.finditer(
                                                 elem.text)),
                                             fillvalue=Str('')))))
                return result


def main(doc=None):
    return run_filter(glossary, doc=doc)


if __name__ == "__main__":
    main()
