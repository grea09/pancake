from panflute import run_filter, Str, RawInline
from itertools import chain, zip_longest
import re

from utils.latex import gls

r = re.compile(r"<([\+-])([^!>]+)>")


def glossary(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Str:
            if r.search(elem.text) is not None:
                def keep(x): return (x.text and (
                    r.match(x.text) == None))

                def parse(m): return RawInline(gls(*m.group(1, 2)), 'latex')
                result = list(filter(keep,
                            chain.from_iterable(
                                zip_longest(
                                    map(Str, re.split(r"<[\+-][^!>]+>", elem.text) + ['']),
                                    map(parse, r.finditer(elem.text)),fillvalue=Str('')
                                )
                            )
                        )
                    )
                return result


def main(doc=None):
    return run_filter(glossary, doc=doc)


if __name__ == "__main__":
    main()
