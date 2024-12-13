import ply.yacc as yacc
from lexer import tokens

# 处理 parallel 语句
def p_statement_parallel(p):
    '''statement : PARALLEL LPAREN IDENTIFIER IN LBRACKET list RBRACKET RPAREN LBRACE statements RBRACE'''
    # 生成并行语句的 AST
    p[0] = {
        'type': 'parallel',
        'variable': p[3],  # x
        'list': p[6],       # [1, 2, 3]
        'body': p[10]        # 语句块
    }

# 处理赋值语句：x = x * 2;
def p_statement_expr(p):
    '''statement : IDENTIFIER EQUALS IDENTIFIER TIMES NUMBER SEMICOLON'''
    p[0] = {
        'type': 'assign',
        'variable': p[1],  # x
        'expr': {
            'type': 'multiply',
            'left': p[3],  # x
            'right': p[5]  # 2
        }
    }

# 处理返回语句：return x;
def p_statement_return(p):
    '''statement : RETURN IDENTIFIER SEMICOLON'''
    p[0] = {
        'type': 'return',
        'value': p[2]  # x
    }

# 处理多个语句
def p_statements(p):
    '''statements : statement statements
                    | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

# 处理列表：[]中的数字
def p_list(p):
    '''list : NUMBER
            | list COMMA NUMBER'''
    if len(p) == 2:
        p[0] = [int(p[1])]
    else:
        p[0] = p[1] + [int(p[3])]

# 错误处理
def p_error(p):
    print(f"Syntax error at '{p.value}'")

# 创建 parser 实例
parser = yacc.yacc()
