import re

from html.parser import HTMLParser
from panflute import run_filter, Table, Math, Para, Str, RawInline

from utils.latex import label, tag

r = re.compile(r"(:.+)?{([^!}]+)}")


class AttributeParser(HTMLParser):
    def handle_startendtag(self, tag, attrs):
        if not hasattr(self, 'attributes'):
            self.attributes = {}
        for key, value in attrs:
            if key.startswith('#'):
                value = key[1:]
                key = 'id'
            if key.startswith('.'):
                value = key[1:]
                if 'class' in self.attributes:
                    value = value + ' ' + self.attributes['class']
                    del self.attributes['class']
                key = 'class'
            self.attributes[key] = value

def attributes(elem, doc):
    if doc.format == 'latex':
        if type(elem) == Table or (type(elem) == Math and elem.format == 'DisplayMath'):
            if type(elem) == Table:
                for a in elem.caption:
                    if type(a) == Str and r.search(a.text) is not None:
                        attrElem = a
                        break
            else:
                attrElem = elem.next
                while type(attrElem) not in [Para, Str]:
                    if attrElem is None:
                        return
                    attrElem = attrElem.next
                if type(attrElem) == Para:
                    for labeltext in attrElem.content:
                        if type(labeltext) == Str:
                            attrElem = labeltext
                            break
            value = attrElem.text
            if r.search(value) is not None:
                attrElem.text = r.sub('', value)
                parser = AttributeParser()
                search = r.search(value)
                parser.feed("<div " + search.group(2) + "/>")
                attributes = parser.attributes
                if search.group(1) and 'name' not in attributes:
                    attributes['name'] = search.group(1)
                if 'id' in attributes:
                    if type(elem) == Table:
                        elem.caption.insert(0, RawInline(label(attributes['id']), 'latex'))
                    if type(elem) == Math:
                        elem.text = label(attributes['id']) + elem.text
                if 'name' in attributes:
                    if type(elem) == Table:
                        for c in elem.caption:
                            if c == attrElem:
                                c.text = r.sub('', value)
                        elem.caption.append(Str(attributes['name']))
                    if type(elem) == Math:
                        elem.text = tag(attributes['name']) + elem.text


def main(doc=None):
    return run_filter(attributes, doc=doc)


if __name__ == "__main__":
    main()
