import re

def sql_lexer(query):
    token_specification = [
        ('SELECT',      r'SELECT\b'),
        ('FROM',        r'FROM\b'),
        ('WHERE',       r'WHERE\b'),
        ('AND',         r'AND\b'),
        ('OR',          r'OR\b'),
        ('COMMA',       r','),
        ('STAR',        r'\*'),
        ('OPERATOR',    r'[<>!=]=?|='),
        ('NUMBER',      r'\d+(\.\d*)?'),
        ('STRING',      r'"[^"]*"|\'[^\']*\''),
        ('IDENTIFIER',  r'[A-Za-z_][A-Za-z0-9_\.]*'),  # supports dot (.)
        ('SKIP',        r'[ \t]+'),
        ('NEWLINE',     r'\n'),
        ('MISMATCH',    r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    tokens = []

    mo = get_token(query, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
            tokens.append(('NUMBER', value))
        elif kind in ('STRING', 'IDENTIFIER', 'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'COMMA', 'OPERATOR', 'STAR'):
            tokens.append((kind, value))
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Unexpected character: {value}")
        pos = mo.end()
        mo = get_token(query, pos)

    return tokens
