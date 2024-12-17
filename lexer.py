import ply.lex as lex

# 保留字
reserved = {
    'const': 'CONST',
    'int': 'INT',
    'void': "VOID",
    'float': 'FLOAT',
    'bool': "BOOL",
    "str": "STR",
    "true": "TRUE",
    "false": "FALSE",
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'getint': 'GETINT',
    'printf': 'PRINTF',
    'parallel': 'PARALLEL',
    'main': 'MAIN',
    'in': 'IN',
    'def': 'DEF',
    'mutex': 'MUTEX',
    'pipe': 'PIPE',
}

# 词法单元
tokens = [
    'IDENTIFIER', 'INTCONST', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'ASSIGN', 'EQUAL', 'NOTEQUAL', 'LESS', 'LESSEQUAL',
    'GREATER', 'GREATEREQUAL', 'LOGICALAND', 'LOGICALOR', 'NOT', 'FORMATSTRING',
    'FLOATCONST', 'STRCONST', 'LSHIFT', 'RSHIFT'
] + list(reserved.values())

# 字面值
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGN = r'='
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATER = r'>'
t_GREATEREQUAL = r'>='
t_LOGICALAND = r'&&'
t_LOGICALOR = r'\|\|'
t_NOT = r'!'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

# 标识符
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # 检查是否为保留字
    return t

def t_FLOATCONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)  # 转换为浮点类型
    return t

# 数值常量
def t_INTCONST(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    return t

def t_STRCONST(t):
    r'"([^"\\]|\\.)*"'  # 匹配字符串字面量，支持转义字符
    t.value = t.value[1:-1]  # 去掉引号
    return t

def t_BOOLCONST(t):
    r'true|false'
    t.value = t.value == 'true'  # 转换为布尔值
    return t

# 忽略空白字符
t_ignore = ' \t'

# 行号处理
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 错误处理
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# 构建 lexer
lexer = lex.lex()

# 词法分析函数
def lex_input(text):
    lexer.input(text)  # 传递源代码给 lexer
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token)
    return tokens
