def to_camel_case(str):
    separators = [' ', '_', '-', '.']
    str = ''.join(s for s in str.title() if not s in separators)
    return str[0].lower() + str[1:]
