from panflute import run_filter, BlockQuote, RawInline

from utils.latex import latex_command

def quote(elem, doc):
    if doc.format == 'latex':
        lettrine = doc.get_metadata('elements')['quote']['title']
        if type(elem) == BlockQuote and lettrine:
            color = ""
            if lettrine['color']:
                color = latex_command('textcolor', lettrine['color'])
            font = ""
            if lettrine['font']:
                font = latex_command(lettrine['font'])
            elem.content[0].content.insert(0, RawInline(
                latex_command('lettrine', color + '{' + font + 
                    lettrine['content'] + '}', lines=lettrine['lines']) + '{}', format='latex'))


def main(doc=None):
    return run_filter(quote, doc=doc)


if __name__ == "__main__":
    main()
