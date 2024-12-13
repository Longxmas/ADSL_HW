import ply.lex as lex

# 保留字表
reserved = {
    'parallel': 'PARALLEL',
    'in': 'IN',
    'return': 'RETURN'
}

# 词法单元列表
tokens = [
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
    'COMMA', 'NUMBER', 'IDENTIFIER', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'SEMICOLON'
] + list(reserved.values())

# 词法规则
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_NUMBER = r'\d+'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_SEMICOLON = r';'  # 添加对分号的支持

# 忽略空格和换行符
t_ignore = ' \t\n'

# 处理保留字
def t_PARALLEL(t):
    r'parallel'
    t.type = reserved.get(t.value, 'PARALLEL')
    return t

def t_IN(t):
    r'in'
    t.type = reserved.get(t.value, 'IN')
    return t

def t_RETURN(t):
    r'return'
    t.type = reserved.get(t.value, 'RETURN')
    return t

# 错误字符处理
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
    
# 创建 lexer 实例
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
