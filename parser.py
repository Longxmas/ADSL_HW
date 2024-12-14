import ply.yacc as yacc
from lexer import tokens

# 用于存储抽象语法树的工具类
class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type  # 节点类型
        self.children = children if children else []  # 子节点
        self.value = value  # 节点值

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value}, children={self.children})"

# 编译单元
def p_CompUnit(p):
    '''CompUnit : Decl CompUnit
                | FuncDef CompUnit
                | MainFuncDef'''
    if len(p) == 3:
        p[0] = ASTNode('CompUnit', [p[1], p[2]])
    else:
        p[0] = ASTNode('CompUnit', [p[1]])

# 声明
def p_Decl(p):
    '''Decl : ConstDecl
            | VarDecl'''
    p[0] = p[1]

def p_ConstDecl(p):
    '''ConstDecl : CONST BType ConstDefList SEMICOLON'''
    p[0] = ASTNode('ConstDecl', [p[2], p[3]])

def p_ConstDefList(p):
    '''ConstDefList : ConstDef
                    | ConstDef COMMA ConstDefList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_ConstDef(p):
    '''ConstDef : IDENTIFIER ASSIGN ConstInitVal
                | IDENTIFIER LBRACKET ConstExp RBRACKET ASSIGN ConstInitVal
                | IDENTIFIER LBRACKET ConstExp RBRACKET LBRACKET ConstExp RBRACKET ASSIGN ConstInitVal'''
    if len(p) == 4:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3]])
    elif len(p) == 6:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3], p[5]])
    else:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3], p[5], p[7], p[9]])

def p_ConstInitVal(p):
    '''ConstInitVal : ConstExp
                    | LBRACE ConstInitValList RBRACE'''
    if len(p) == 2:
        p[0] = ASTNode('ConstInitVal', [p[1]])
    else:
        p[0] = ASTNode('ConstInitVal', p[2])

def p_ConstInitValList(p):
    '''ConstInitValList : ConstInitVal
                        | ConstInitVal COMMA ConstInitValList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_ConstExp(p):
    '''ConstExp : AddExp'''
    p[0] = ASTNode('ConstExp', [p[1]])

# 基本类型
def p_BType(p):
    '''BType : INT'''
    p[0] = ASTNode('BType', value=p[1])

# 变量声明
def p_VarDecl(p):
    '''VarDecl : BType VarDef SEMICOLON
               | BType VarDef COMMA VarDef SEMICOLON'''
    if len(p) == 4:
        p[0] = ASTNode('VarDecl', [p[1], p[2]])
    else:
        p[0] = ASTNode('VarDecl', [p[1], p[2], p[4]])

# 变量定义
def p_VarDef(p):
    '''VarDef : IDENTIFIER
              | IDENTIFIER ASSIGN InitVal
              | IDENTIFIER LBRACKET ConstExp RBRACKET
              | IDENTIFIER LBRACKET ConstExp RBRACKET ASSIGN InitVal'''
    if len(p) == 2:
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1])])
    elif len(p) == 4:
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[3]])
    elif len(p) == 5:
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[3]])
    else:
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[3], p[6]])

# 变量初值
def p_InitVal(p):
    '''InitVal : Exp
               | LBRACE InitVal RBRACE'''
    if len(p) == 2:
        p[0] = ASTNode('InitVal', [p[1]])
    else:
        p[0] = ASTNode('InitVal', [p[2]])

# 表达式
def p_Exp(p):
    '''Exp : AddExp'''
    p[0] = p[1]
    
def p_LOrExp(p):
    '''LOrExp : LAndExp
              | LOrExp LOGICALOR LAndExp'''
    if len(p) == 2:
        # 单个逻辑与表达式
        p[0] = p[1]
    else:
        # 逻辑或运算
        p[0] = ASTNode('LOrExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

def p_LAndExp(p):
    '''LAndExp : EqExp
               | LAndExp LOGICALAND EqExp'''
    if len(p) == 2:
        # 单个相等性表达式
        p[0] = p[1]
    else:
        # 逻辑与运算
        p[0] = ASTNode('LAndExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 加减表达式
def p_AddExp(p):
    '''AddExp : MulExp
              | AddExp PLUS MulExp
              | AddExp MINUS MulExp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('AddExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 乘除模表达式
def p_MulExp(p):
    '''MulExp : UnaryExp
              | MulExp TIMES UnaryExp
              | MulExp DIVIDE UnaryExp
              | MulExp MOD UnaryExp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('MulExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# EqExp (相等性表达式)
def p_EqExp(p):
    '''EqExp : RelExp
             | EqExp EQUAL RelExp
             | EqExp NOTEQUAL RelExp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('EqExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# RelExp (关系表达式)
def p_RelExp(p):
    '''RelExp : AddExp
              | RelExp LESS AddExp
              | RelExp LESSEQUAL AddExp
              | RelExp GREATER AddExp
              | RelExp GREATEREQUAL AddExp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('RelExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 一元表达式
def p_UnaryExp(p):
    '''UnaryExp : PrimaryExp
                | IDENTIFIER LPAREN FuncRParams RPAREN
                | UnaryOp UnaryExp'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ASTNode('Call', [ASTNode('Ident', value=p[1]), p[3]])
    else:
        p[0] = ASTNode('UnaryExp', [p[1], p[2]])

# 单目运算符
def p_UnaryOp(p):
    '''UnaryOp : PLUS
               | MINUS
               | NOT'''
    p[0] = ASTNode('UnaryOp', value=p[1])

# 基本表达式
def p_PrimaryExp(p):
    '''PrimaryExp : LPAREN Exp RPAREN
                  | LVal
                  | INTCONST'''
    if len(p) == 4:
        p[0] = p[2]
    elif isinstance(p[1], int):
        p[0] = ASTNode('IntConst', value=p[1])
    else:
        p[0] = p[1]

# 左值表达式
def p_LVal(p):
    '''LVal : IDENTIFIER
            | IDENTIFIER LBRACKET Exp RBRACKET'''
    if len(p) == 2:
        p[0] = ASTNode('LVal', [ASTNode('Ident', value=p[1])])
    else:
        p[0] = ASTNode('LVal', [ASTNode('Ident', value=p[1]), p[3]])

# 主函数定义
def p_MainFuncDef(p):
    '''MainFuncDef : INT MAIN LPAREN RPAREN Block'''
    p[0] = ASTNode('MainFuncDef', [p[5]])

# 语句
def p_Stmt(p):
    '''Stmt : LVal ASSIGN Exp SEMICOLON
            | Exp SEMICOLON
            | SEMICOLON
            | Block
            | IF LPAREN Cond RPAREN Stmt ELSE Stmt
            | IF LPAREN Cond RPAREN Stmt
            | FOR LPAREN ForStmt SEMICOLON Cond SEMICOLON ForStmt RPAREN Stmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | RETURN Exp SEMICOLON
            | RETURN SEMICOLON
            | LVal ASSIGN GETINT LPAREN RPAREN SEMICOLON
            | PRINTF LPAREN FormatString PRINTFParams RPAREN SEMICOLON
            | PARALLEL LPAREN IDENTIFIER IN LBRACKET list RBRACKET RPAREN Block'''
    if len(p) == 5 and p[2] == '=':
        # LVal '=' Exp ';'
        p[0] = ASTNode('AssignStmt', [p[1], p[3]])
    elif len(p) == 3 and p[1] != ';':
        # Exp ';'
        p[0] = ASTNode('ExpStmt', [p[1]])
    elif len(p) == 2 and p[1] == ';':
        # Empty statement
        p[0] = ASTNode('EmptyStmt')
    elif len(p) == 2:
        # Block
        p[0] = p[1]
    elif len(p) == 8:
        # IF '(' Cond ')' Stmt ELSE Stmt
        p[0] = ASTNode('IfStmt', [p[3], p[5], p[7]])
    elif len(p) == 6:
        # IF '(' Cond ')' Stmt
        p[0] = ASTNode('IfStmt', [p[3], p[5]])
    elif len(p) == 10 and p[1] == "for":
        # FOR '(' [ForStmt] ';' [Cond] ';' [ForStmt] ')' Stmt
        p[0] = ASTNode('ForStmt', [p[3], p[5], p[7], p[9]])
    elif len(p) == 3 and p[1] == 'break':
        # 'break' ';'
        p[0] = ASTNode('BreakStmt')
    elif len(p) == 3 and p[1] == 'continue':
        # 'continue' ';'
        p[0] = ASTNode('ContinueStmt')
    elif len(p) == 4 and p[1] == 'return':
        # 'return' Exp ';'
        p[0] = ASTNode('ReturnStmt', [p[2]])
    elif len(p) == 3 and p[1] == 'return':
        # 'return' ';'
        p[0] = ASTNode('ReturnStmt')
    elif len(p) == 7:
        # LVal '=' 'getint' '(' ')' ';'
        p[0] = ASTNode('GetIntStmt', [p[1]])
    elif len(p) == 8:
        # 'printf' '(' FormatString PRINTFParams ')' ';'
        p[0] = ASTNode('PrintfStmt', [p[3], p[4]])
    elif len(p) == 10 and p[1] == "parallel":
        # 'parallel' '(' IDENTIFIER 'in' LBRACKET list RBRACKET ')' Block
        p[0] = ASTNode('ParallelStmt', [ASTNode('Ident', value=p[3]), p[6], p[9]])

# 修正后的定义
def p_PRINTFParams(p):
    '''PRINTFParams : Exp
                    | Exp COMMA PRINTFParams'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_PRINTFParams_empty(p):
    '''PRINTFParams : '''
    p[0] = []

# ForStmt
def p_ForStmt(p):
    '''ForStmt : LVal ASSIGN Exp
               | '''
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = ASTNode('ForAssign', [p[1], p[3]])

# 并行语句的列表部分
def p_list(p):
    '''list : Exp
            | list COMMA Exp'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# FuncDef (函数定义)
def p_FuncDef(p):
    '''FuncDef : DEF IDENTIFIER LPAREN FuncFParams RPAREN Block
               | DEF IDENTIFIER LPAREN RPAREN Block'''
    if len(p) == 7:
        # 函数定义，有形参
        p[0] = ASTNode('FuncDef', [ASTNode('Ident', value=p[2]), p[4], p[6]])
    else:
        # 函数定义，无形参
        p[0] = ASTNode('FuncDef', [ASTNode('Ident', value=p[2]), p[5]])

# FuncFParams (函数形参列表)
def p_FuncFParams(p):
    '''FuncFParams : FuncFParam
                   | FuncFParam COMMA FuncFParams'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# FuncFParam (单个形参)
def p_FuncFParam(p):
    '''FuncFParam : IDENTIFIER'''
    p[0] = ASTNode('FuncFParam', [ASTNode('Ident', value=p[1])])


# FuncRParams （函数实参）
def p_FuncRParams(p):
    '''FuncRParams : Exp
                   | Exp COMMA FuncRParams'''
    if len(p) == 2:
        # 单个参数
        p[0] = [p[1]]
    else:
        # 多个参数
        p[0] = [p[1]] + p[3]

def p_Block(p):
    '''Block : LBRACE RBRACE
             | LBRACE BlockItems RBRACE'''
    if len(p) == 3:
        # 空的 Block
        p[0] = ASTNode('Block', [])
    else:
        # 包含多个 BlockItem 的 Block
        p[0] = ASTNode('Block', p[2])

def p_BlockItems(p):
    '''BlockItems : BlockItem
                  | BlockItem BlockItems'''
    if len(p) == 2:
        # 单个 BlockItem
        p[0] = [p[1]]
    else:
        # 多个 BlockItem
        p[0] = [p[1]] + p[2]

def p_BlockItem(p):
    '''BlockItem : Decl
                 | Stmt'''
    p[0] = p[1]


def p_Cond(p):
    '''Cond : LOrExp'''
    p[0] = ASTNode('Cond', [p[1]])

# FormatString 的解析规则
def p_FormatString(p):
    '''FormatString : FORMATSTRING'''
    p[0] = ASTNode('FormatString', value=p[1])


# 错误处理
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, line {p.lineno}")
    else:
        print("Syntax error at EOF")


# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# 构建 Parser
parser = yacc.yacc(debug=True, debuglog=log)


def format_ast(node, indent=0):
    """
    按指定格式递归打印 AST。
    :param node: 当前 ASTNode 节点
    :param indent: 缩进层级
    :return: 格式化字符串
    """
    if not isinstance(node, ASTNode):
        return repr(node)  # 对非 ASTNode 类型直接返回字符串表示

    # 打印当前节点的信息
    indent_str = " " * (indent * 4)  # 每个层级缩进 4 个空格
    result = f"{indent_str}ASTNode(type='{node.type}',"
    if node.value is not None:
        result += f" value='{node.value}',"
    result += f" children=["

    # 递归打印子节点
    if isinstance(node.children, list) and node.children:
        children_str = []
        for child in node.children:
            child_str = format_ast(child, indent + 1)  # 子节点递归缩进
            children_str.append(child_str)
        result += "\n" + ",\n".join(children_str) + f"\n{indent_str}]"
    else:
        result += "]"  # 无子节点的情况
    result += ")"
    return result
