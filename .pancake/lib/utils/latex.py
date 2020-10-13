from panflute import RawBlock, stringify


def latex_command(name, content='', **kwargs):
    options = ''
    if 'option' in kwargs:
        options = kwargs['option']
        del kwargs['option']
    for key, value in kwargs.items():
        options += ('' if options == '' else ',') + key + '=' + value
    return '\\' + name + brakets(options) + braces(content)


def image(url, **kwargs):
    return latex_command('includegraphics', url, **kwargs)


def begin(x):
    return latex_command('begin', x)


def end(x):
    return latex_command('end', x)


def braces(x):
    if x == '':
        return ''
    else:
        return '{' + x + '}'


def brakets(x):
    if x == '':
        return ''
    else:
        return '[' + x + ']'


def parentesis(x):
    if x == '':
        return ''
    else:
        return '(' + x + ')'


def caption(x):
    if not x:
        return ''
    return latex_command('caption', x)


def captionof(x):
    if not x:
        return ''
    return latex_command('captionof{figure}', x)


def label(x, *args, **kwargs):
    if not x:
        return ''
    if len(args) >= 1:
        return latex_command('label', x, option=args[0])
    else:
        return latex_command('label', x)


def tag(x, simple=False):
    return latex_command('tag' + '*' if simple else '', x)


def gls(entry, glsid):
    command = 'Gls' if glsid.isupper() else 'gls'
    if entry == '-':
        command += 'entry'
        command += 'plural' if (glsid.endswith('S')) else 'name'
    elif entry == '+':
        command += 'pl' if (glsid.endswith('S')) else ''
    glsid = glsid.lower()[:-1] if (glsid.endswith('S')) else glsid.lower()
    return latex_command(command, glsid)
