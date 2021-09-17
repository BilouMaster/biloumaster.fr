# removes empty lines
def str_clean(text: str) -> str:
    return '\n'.join([line for line in text.split('\n') if line.strip()])