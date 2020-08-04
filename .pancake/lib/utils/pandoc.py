from pandocfilters import stringify, walk

def getMeta(meta, key):
    # Return a structured data from a key
    # as defined in the meta
    if key in meta:
        return decodeMeta(meta[key])


def decodeMeta(meta):
    # Return a structured data as defined in the meta
    # if not hasattr(getMap, 'value'):
    decode = {
        'MetaBool': bool,
        'MetaInlines': stringify,
        'MetaList': decodeList,
        'MetaMap': decodeMap,
    }
    return decode[meta['t']](meta['c'])


def decodeList(metaList):
    # Return a list as encoded in the meta
    result = []
    for value in metaList:
        result.append(decodeMeta(value))
    return result


def decodeMap(metaMap):
    # Return a dict as encoded in the meta
    result = {}
    for key, value in metaMap.items():
        result[key] = decodeMeta(value)
    return result


def raw(x):
    result = []

    def flatten(key, val, format, meta):
        if val is not None:
            if isinstance(val[1], unicode):
                result.append(val[1])
            if isinstance(val[1], dict):
                result.append(" ")
    walk(x, flatten, "", {})
    return ''.join(result)
