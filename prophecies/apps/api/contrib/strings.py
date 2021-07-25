def to_camel_case(str):
    str = ''.join(s for s in str.title() if not s == '_')
    return str[0].lower() + str[1:]
