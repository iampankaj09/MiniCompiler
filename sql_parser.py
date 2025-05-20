from core.sql_lexer import sql_lexer

def sql_parser(query):
    tokens = sql_lexer(query)
    parsed = {'columns': [], 'table': '', 'where': None}
    i = 0

    while i < len(tokens):
        kind, value = tokens[i]

        if kind == 'SELECT':
            i += 1
            if tokens[i][0] == 'STAR':
                parsed['columns'] = '*'
                i += 1
            else:
                while tokens[i][0] != 'FROM':
                    if tokens[i][0] == 'IDENTIFIER':
                        parsed['columns'].append(tokens[i][1])
                    i += 1

        elif kind == 'FROM':
            i += 1
            if tokens[i][0] == 'IDENTIFIER':
                table_name = tokens[i][1]
                parsed['table'] = table_name
                parsed['filename'] = table_name if table_name.endswith('.csv') else f"{table_name}.csv"
                i += 1

        elif kind == 'WHERE':
            i += 1
            left = tokens[i][1]; i += 1
            op = tokens[i][1]; i += 1
            right = tokens[i][1]; i += 1
            parsed['where'] = (left, op, right)

        else:
            i += 1

    return parsed
