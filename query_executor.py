import pandas as pd
from core.sql_parser import sql_parser

def query_executor(query):
    parsed = sql_parser(query)

    try:
        df = pd.read_csv(parsed['filename'])
    except FileNotFoundError:
        return f"File not found: {parsed['filename']}"

    # WHERE condition
    if parsed['where']:
        field, op, value = parsed['where']
        if df[field].dtype == 'object':
            value = str(value).strip('"').strip("'")
        else:
            value = float(value)

        if op == '=':
            df = df[df[field] == value]
        elif op == '>':
            df = df[df[field] > value]
        elif op == '<':
            df = df[df[field] < value]
        elif op == '>=':
            df = df[df[field] >= value]
        elif op == '<=':
            df = df[df[field] <= value]
        elif op == '!=':
            df = df[df[field] != value]

    # Column selection
    try:
        if parsed['columns'] == '*':
            result = df
        else:
            result = df[parsed['columns']]
    except KeyError:
        return f"Column(s) not found: {parsed['columns']}"

    return result.to_string(index=False)
