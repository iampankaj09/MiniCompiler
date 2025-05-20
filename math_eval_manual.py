import re

def tokenize(expr):
    return re.findall(r'\d+\.?\d*|[+\-*/()]', expr)

def evaluate(expression):
    def precedence(op): return {'+':1, '-':1, '*':2, '/':2}.get(op, 0)
    def apply(op, b, a):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b

    tokens = tokenize(expression)
    values, ops = [], []

    for token in tokens:
        if re.match(r'\d+\.?\d*', token):
            values.append(float(token))
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                values.append(apply(ops.pop(), values.pop(), values.pop()))
            ops.pop()
        else:
            while ops and precedence(ops[-1]) >= precedence(token):
                values.append(apply(ops.pop(), values.pop(), values.pop()))
            ops.append(token)

    while ops:
        values.append(apply(ops.pop(), values.pop(), values.pop()))

    return values[0]
