from panflute import RawBlock, stringify


def latex_command(name, content, **kwargs):
    if content == '':
        return ''
    else:
        return '\\' + name + (('[' + kwargs.get('option') + ']')
                              if 'option' in kwargs else '') + '{' + content + '}'


def tcb(properties, definedClass, id, content):
    param = ''
    name = ''
    if 'name' in properties:
        name = properties['name']
    if 'param' in properties:
        param = properties['param']
    if not id:
        id = definedClass + str(hash(stringify(content)))
    return [RawBlock('latex', begin(definedClass) + brakets(param) + braces(param) + braces(id))] + content + [RawBlock('latex', end(definedClass))]


def block(properties, definedClass, id, content):
    param = ''
    name = ''
    if 'name' in properties:
        name = properties['name']
    if 'param' in properties:
        param = properties['param']
    return [RawBlock('latex', begin(definedClass) + brakets(name) + braces(param) + label(id))] + content + [RawBlock('latex', end(definedClass))]


def image(url):
    return latex_command('includegraphics', url)


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
    return latex_command('caption', x)


def captionof(x):
    return latex_command('captionof{figure}', x)


def label(x, *args, **kwargs):
    if len(args) >= 1:
        return latex_command('label', x, option=args[0])
    else:
        return latex_command('label', x)


def gls(entry, glsid):
    command = 'Gls' if glsid.isupper() else 'gls'
    if entry == '-':
        command += 'entry'
        command += 'name' if (glsid.endswith('S')) else 'plural'
    elif entry == '+':
        command += 'pl' if (glsid.endswith('S')) else ''
    glsid = glsid.lower()[:-1] if (glsid.endswith('S')) else glsid.lower()
    return latex_command(command, glsid)
