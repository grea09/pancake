import re
from html.parser import HTMLParser
from panflute import run_filter, Table, Math, Str

r = re.compile(r"{([^!}]+)}")


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


def nextAttributes(elem, doc):
    index = doc.content.index(elem)
    for i in range(index+1, len(doc.content)-1):
        if type(doc.content[i]) == Str:
            value = doc.content[i].content
            if r.search(value) is not None:
                doc.content[i].content = r.sub('', value)
                parser = AttributeParser()
                parser.feed("<div " + r.search(value).group(1) + "/>")
                return parser.attributes


def attributes(elem, doc):
    if doc.format == 'latex':
        if type(elem) in {Table, Math}:
            attributes = nextAttributes(elem, doc)
            if 'id' in attributes:
                elem.id = attributes['id']
                del attributes['id']
            if 'class' in attributes:
                elem.classes.append(attributes['class'].split())
                del attributes['class']
            elem.attributes = {**elem.attributes, **attributes}


def main(doc=None):
    return run_filter(attributes, doc=doc)


if __name__ == "__main__":
    main()
