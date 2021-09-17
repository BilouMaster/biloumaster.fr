def str_indent(text:str, level: int, char=' ', size=4) -> str:
    return ('\n' + char * size * level).join(text.split('\n'))