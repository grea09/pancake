#!/usr/bin/env python

"""
Pandoc filter to add glossary capabilities
"""

from utils import *
from html.parser import HTMLParser
import re
import tempfile
import os
import pickle
import logging

from pandocfilters import toJSONFilter, Str, Math, Table

constr = {"Math":Math, "Table":Table}
tmp = "/tmp/pancake_attributes.pkl"

def pancake_glossary(key, value, format, meta):
    if format == "latex":
        if key in ['Math', 'Table']:
            if key == 'Math' and value[0]['t'] != 'DisplayMath':
                return
            if os.path.exists(tmp):
                attributes = _load()
                _del()
                logging.warning("loaded attributes=%s", attributes)
                if len(value[0]) > 1:
                    [[id, classes, properties], content] = value
                else:
                    logging.warning("existing value=%s", value)
                    id=''
                    classes=[]
                    properties=value[0]
                    content=value[1]
                
                if 'id' in attributes:
                    id = attributes['id']
                    del attributes['id']
                if 'class' in attributes:
                    classes.append(attributes['class'].split())
                    del attributes['class']
                properties = {**properties, **attributes}
                return constr[key]([[id, classes, properties], content])
        elif key == 'Str':
            r = re.compile(r"{([^!}]+)}")
            if r.search(value) is not None:
                result = r.sub('', value)
                parser = AttributeParser()
                parser.feed("<div " + r.search(value).group(1) + "/>")
                _save(parser.attributes)
                logging.warning("saved attributes=%s", parser.attributes)
                return Str(result)


class AttributeParser(HTMLParser):

    def handle_startendtag(self, tag, attrs):
        if not hasattr(self,'attributes'):
            self.attributes = {}
        for key, value in attrs:
            if key.startswith('#'):
                value= key[1:]
                key= 'id'
            if key.startswith('.'):
                value= key[1:]
                if 'class' in self.attributes:
                    value = value + ' ' + self.attributes['class']
                key= 'class'
            self.attributes[key] = value

def _save(obj):
    with open(tmp, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def _del():
    if os.path.exists(tmp):
        os.remove(tmp)

def _load():
    with open(tmp, 'rb') as f:
        return pickle.load(f)   

if __name__ == '__main__':
    toJSONFilter(pancake_glossary)
