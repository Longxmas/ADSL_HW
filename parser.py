import ply.yacc as yacc
from lexer import tokens
from util import ASTNode

# 用于存储抽象语法树的工具类
# class ASTNode:
#     def __init__(self, type, child_nodes=None, value=None):
#         self.type = type  # 节点类型
#         self.child_nodes = child_nodes if child_nodes else []  # 子节点
#         self.value = value  # 节点值
#
#     def __repr__(self):
#         return f"ASTNode(type={self.type}, value={self.value}, child_nodes={self.child_nodes})"

# 编译单元
def p_CompUnit(p):
    '''CompUnit : Decls FuncDefs MainFuncDef
                | Decls MainFuncDef
                | FuncDefs MainFuncDef
                | MainFuncDef'''
    if len(p) == 4:
        # 包含声明、函数定义和主函数
        p[0] = ASTNode('CompUnit', [p[1], p[2], p[3]])
    elif len(p) == 3:
        # 包含声明或函数定义，以及主函数
        p[0] = ASTNode('CompUnit', [p[1], p[2]])
    else:
        # 仅包含主函数
        p[0] = ASTNode('CompUnit', [p[1]])

def p_Decls(p):
    '''Decls : Decl Decls
             | Decl'''
    if len(p) == 2:
        p[0] = ASTNode('Decls', [p[1]])
    else:
        p[0] = ASTNode('Decls', [p[1]] + p[2].child_nodes)

# 声明
def p_Decl(p):
    '''Decl : ConstDecl
            | VarDecl'''
    p[0] = ASTNode('Decl', [p[1]])

def p_ConstDecl(p):
    '''ConstDecl : CONST BType ConstDefList SEMICOLON'''
    p[0] = ASTNode('ConstDecl', [p[2], p[3]])

def p_ConstDefList(p):
    '''ConstDefList : ConstDef
                    | ConstDef COMMA ConstDefList'''
    if len(p) == 2:
        p[0] = ASTNode('ConstDefList', [p[1]])
    else:
        p[0] = ASTNode('ConstDefList', [p[1]] + p[3].child_nodes)

def p_ConstDef(p):
    '''ConstDef : IDENTIFIER ASSIGN ConstInitVal
                | IDENTIFIER LBRACKET ConstExp RBRACKET ASSIGN ConstInitVal
                | IDENTIFIER LBRACKET ConstExp RBRACKET LBRACKET ConstExp RBRACKET ASSIGN ConstInitVal'''
    if len(p) == 4:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3]])
    elif len(p) == 7:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3], p[6]])
    else:
        p[0] = ASTNode('ConstDef', [ASTNode('Ident', value=p[1]), p[3], p[6], p[9]])

def p_ConstInitVal(p):
    '''ConstInitVal : ConstExp
                    | LBRACE ConstInitValList RBRACE'''
    if len(p) == 2:
        p[0] = ASTNode('ConstInitVal', [p[1]])
    else:
        p[0] = ASTNode('ConstInitVal', [p[2]])

def p_ConstInitValList(p):
    '''ConstInitValList : ConstInitVal
                        | ConstInitVal COMMA ConstInitValList'''
    if len(p) == 2:
        p[0] = ASTNode('ConstInitValList', [p[1]])
    else:
        p[0] = ASTNode('ConstInitValList', [p[1]] + p[3].child_nodes)

def p_ConstExp(p):
    '''ConstExp : AddExp'''
    p[0] = ASTNode('ConstExp', [p[1]])

# 基本类型
def p_BType(p):
    '''BType : INT
             | BOOL
             | FLOAT
             | STR
             | PIPE INT  
             | PIPE BOOL  
             | PIPE FLOAT'''
    if len(p) == 2:
        p[0] = ASTNode('BType', value=p[1])
    elif len(p) == 3:
        p[0] = ASTNode('BType', value=p[1] + ' ' + p[2])

# 基本类型
def p_FuncBType(p):
    '''FuncBType : INT
                | BOOL
                | FLOAT
                | STR
                | VOID'''
    if len(p) == 2:
        p[0] = ASTNode('FuncBType', value=p[1])

# 变量声明
def p_VarDecl(p):
    '''VarDecl : BType VarDefList SEMICOLON'''
    p[0] = ASTNode('VarDecl', [p[1], p[2]])

def p_VarDefList(p):
    '''VarDefList : VarDef
                  | VarDef COMMA VarDefList'''
    if len(p) == 2:
        # 单个变量定义
        p[0] = ASTNode('VarDefList', [p[1]])
    else:
        # 多个变量定义
        p[0] = ASTNode('VarDefList', [p[1]] + p[3].child_nodes)

# 变量定义
def p_VarDef(p):
    '''VarDef : IDENTIFIER
              | IDENTIFIER ArrayDimensions
              | IDENTIFIER ASSIGN InitVal
              | IDENTIFIER ArrayDimensions ASSIGN InitVal'''
    if len(p) == 2:
        # 普通变量
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1])])
    elif len(p) == 3:
        # 多维数组
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[2]])
    elif len(p) == 4:
        # print(f"vardef {p[1], p[2], p[3]}")
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[3]])
    else:
        p[0] = ASTNode('VarDef', [ASTNode('Ident', value=p[1]), p[2], p[4]])

def p_ArrayDimensions(p):
    '''ArrayDimensions : LBRACKET ConstExp RBRACKET
                       | ArrayDimensions LBRACKET ConstExp RBRACKET'''
    if len(p) == 4:
        # 单维数组 `[ConstExp]`
        p[0] = ASTNode('ArrayDimensions', children=[p[2]])
    else:
        # 多维数组 `[ConstExp][ConstExp]...`
        p[0] = ASTNode('ArrayDimensions', children=p[1].child_nodes + [p[3]])

# 变量初值
def p_InitVal(p):
    '''InitVal : Exp
               | LBRACE InitValList RBRACE'''
    if len(p) == 2:
        # 单一值初始化
        p[0] = ASTNode('InitVal', [p[1]])
    else:
        # 多维数组初始化
        p[0] = ASTNode('InitVal', [p[2]])

def p_InitValList(p):
    '''InitValList : InitVal
                   | InitVal COMMA InitValList'''
    if len(p) == 2:
        p[0] = ASTNode('InitValList', [p[1]])
    else:
        p[0] = ASTNode('InitValList', [p[1]] + p[3].child_nodes)

# 表达式
def p_Exp(p):
    '''Exp : AddExp'''
    p[0] = ASTNode('Exp', [p[1]])
    
def p_LOrExp(p):
    '''LOrExp : LAndExp
              | LOrExp LOGICALOR LAndExp'''
    if len(p) == 2:
        # 单个逻辑与表达式
        p[0] = ASTNode('LOrExp', [p[1]])
    else:
        # 逻辑或运算
        p[0] = ASTNode('LOrExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

def p_LAndExp(p):
    '''LAndExp : EqExp
               | LAndExp LOGICALAND EqExp'''
    if len(p) == 2:
        # 单个相等性表达式
        p[0] = ASTNode('LAndExp', [p[1]])
    else:
        # 逻辑与运算
        p[0] = ASTNode('LAndExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 加减表达式
def p_AddExp(p):
    '''AddExp : MulExp
              | AddExp PLUS MulExp
              | AddExp MINUS MulExp'''
    if len(p) == 2:
        p[0] = ASTNode('AddExp', [p[1]])
    else:
        p[0] = ASTNode('AddExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 乘除模表达式
def p_MulExp(p):
    '''MulExp : UnaryExp
              | MulExp TIMES UnaryExp
              | MulExp DIVIDE UnaryExp
              | MulExp MOD UnaryExp'''
    if len(p) == 2:
        p[0] = ASTNode('MulExp', [p[1]])
    else:
        p[0] = ASTNode('MulExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# EqExp (相等性表达式)
def p_EqExp(p):
    '''EqExp : RelExp
             | EqExp EQUAL RelExp
             | EqExp NOTEQUAL RelExp'''
    if len(p) == 2:
        p[0] = ASTNode('EqExp', [p[1]])
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
        p[0] = ASTNode('RelExp', [p[1]])
    else:
        p[0] = ASTNode('RelExp', [p[1], ASTNode('Op', value=p[2]), p[3]])

# 一元表达式
def p_UnaryExp(p):
    '''UnaryExp : PrimaryExp
                | IDENTIFIER LPAREN FuncRParams RPAREN
                | UnaryOp UnaryExp'''
    if len(p) == 2:
        p[0] = ASTNode('UnaryExp', [p[1]])
    elif len(p) == 5:
        p[0] = ASTNode('UnaryExp', [ASTNode('Ident', value=p[1]), p[3]])
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
                  | INTCONST
                  | FLOATCONST
                  | STRCONST
                  | TRUE
                  | FALSE'''
    if len(p) == 4:
        # 带括号的表达式
        p[0] = ASTNode('PrimaryExp', [p[2]])
    elif p.slice[1].type == 'LVal':
        # 左值表达式
        p[0] = ASTNode('PrimaryExp', [p[1]])
    elif p.slice[1].type == 'TRUE':
        # 布尔常量 true
        p[0] = ASTNode('PrimaryExp', [ASTNode('BoolConst', value=p[1])])
    elif p.slice[1].type == 'FALSE':
        # 布尔常量 false
        p[0] = ASTNode('PrimaryExp', [ASTNode('BoolConst', value=p[1])])
    elif p.slice[1].type == 'INTCONST':
        # 整型常量
        p[0] = ASTNode('PrimaryExp', [ASTNode('IntConst', value=p[1])])
    elif p.slice[1].type == 'FLOATCONST':
        # 浮点数常量
        p[0] = ASTNode('PrimaryExp', [ASTNode('FloatConst', value=p[1])])
    elif p.slice[1].type == 'STRCONST':
        # 字符串常量
        p[0] = ASTNode('PrimaryExp', [ASTNode('StrConst', value=p[1])])


# 左值表达式
def p_LVal(p):
    '''LVal : IDENTIFIER
            | IDENTIFIER ArrayDimensions'''
    if len(p) == 2:
        p[0] = ASTNode('LVal', [ASTNode('Ident', value=p[1])])
    else:
        p[0] = ASTNode('LVal', [ASTNode('Ident', value=p[1]), p[2]])

# 主函数定义
def p_MainFuncDef(p):
    '''MainFuncDef : VOID MAIN LPAREN RPAREN Block'''
    p[0] = ASTNode('MainFuncDef', [p[5]])

# 语句
def p_Stmt(p):
    '''Stmt : LVal ASSIGN Exp SEMICOLON
            | Exp SEMICOLON
            | SEMICOLON
            | Block
            | IF LPAREN Cond RPAREN Stmt ELSE Stmt
            | IF LPAREN Cond RPAREN Stmt
            | FOR IDENTIFIER IN IDENTIFIER Stmt
            | FOR LPAREN ForExp SEMICOLON Cond SEMICOLON ForExp RPAREN Stmt
            | FOR LPAREN ForExp SEMICOLON SEMICOLON ForExp RPAREN Stmt
            | FOR LPAREN ForExp SEMICOLON Cond SEMICOLON RPAREN Stmt
            | FOR LPAREN SEMICOLON Cond SEMICOLON ForExp RPAREN Stmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | RETURN Exp SEMICOLON
            | RETURN SEMICOLON
            | LVal LSHIFT Exp SEMICOLON
            | LVal RSHIFT Exp SEMICOLON
            | LVal RSHIFT SEMICOLON
            | PRINTF LPAREN STRCONST RPAREN SEMICOLON
            | PRINTF LPAREN STRCONST PRINTFParams RPAREN SEMICOLON
            | SCANF  LPAREN STRCONST PRINTFParams RPAREN SEMICOLON
            | PARALLEL LPAREN FuncFParams RPAREN IN ParallelRealList Block'''
    if len(p) == 5 and p[2] == '=':
        # LVal '=' Exp ';'
        p[0] = ASTNode('AssignStmt', [p[1], p[3]])
    elif len(p) == 5 and p[2] == '<<':
        # LVal '<<' Exp ';'
        p[0] = ASTNode('ShiftLeftStmt', [p[1], p[3]])
    elif len(p) == 5 and p[2] == '>>':
        # Lval '>>' Exp ';'
        p[0] = ASTNode('ShiftRightStmt', [p[1], p[3]])
    elif len(p) == 4 and p[2] == '>>':
        # Lval '>>' ';'
        p[0] = ASTNode('ShiftRightStmt', [p[1]])
    elif len(p) == 3 and p[1] != ';' and p[1] != "return":
        # Exp ';'
        p[0] = ASTNode('ExpStmt', [p[1]])
    elif len(p) == 2 and p[1] == ';':
        # Empty statement
        p[0] = ASTNode('EmptyStmt')
    elif len(p) == 2:
        # Block
        p[0] = ASTNode('BlockStmt', [p[1]])
    elif len(p) == 8 and p[1] == "if":
        # IF '(' Cond ')' Stmt ELSE Stmt
        p[0] = ASTNode('IfStmt', [p[3], p[5], p[7]])
    elif len(p) == 6 and p[1] == "if":
        # IF '(' Cond ')' Stmt
        p[0] = ASTNode('IfStmt', [p[3], p[5]])
    elif len(p) == 6 and p[1] == "for":
        # FOR IDENTIFIER IN IDENTIFIER Stmt
        p[0] = ASTNode('ForStmt', [ASTNode('Ident', value=p[2]), ASTNode('Ident', value=p[4]), p[5]])
    elif len(p) == 10 and p[1] == "for":
        # FOR LPAREN ForExp SEMICOLON Cond SEMICOLON ForExp RPAREN Stmt
        p[0] = ASTNode('ForStmt', [p[3], p[5], p[7], p[9]])
    elif len(p) == 9 and p[1] == "for" and p[4] == ";" and p[5] == ";":
        # FOR LPAREN ForExp SEMICOLON SEMICOLON ForExp RPAREN Stmt
        p[0] = ASTNode('ForStmt', [p[3], p[6], p[8]])
    elif len(p) == 9 and p[1] == "for" and p[4] == ";" and p[6] == ";":
        # FOR LPAREN ForExp SEMICOLON Cond SEMICOLON RPAREN Stmt
        p[0] = ASTNode('ForStmt', [p[3], p[5], p[8]])
    elif len(p) == 9 and p[1] == "for" and p[3] == ";" and p[5] == ";":
        # FOR LPAREN SEMICOLON Cond SEMICOLON ForExp RPAREN Stmt
        p[0] = ASTNode('ForStmt', [p[4], p[6], p[8]])
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
        p[0] = ASTNode('ReturnStmt', [])
    elif len(p) == 7 and p[1] == "scanf":
        # 'scanf' '(' STRCONST PRINTFParams ')' ';'
        p[0] = ASTNode('ScanfStmt', [ASTNode('STRCONST', value=p[3]), p[4]])
    elif len(p) == 6 and p[1] == "printf":
        # 'printf' '(' STRCONST ')' ';'
        p[0] = ASTNode('PrintfStmt', [ASTNode('STRCONST', value=p[3])])
    elif len(p) == 7 and p[1] == "printf":
        # 'printf' '(' STRCONST PRINTFParams ')' ';'
        p[0] = ASTNode('PrintfStmt', [ASTNode('STRCONST', value=p[3]), p[4]])
    elif len(p) == 8 and p[1] == "parallel":
        # 'parallel' '(' FuncFParams ')' 'in' ParallelRealList Block
        p[0] = ASTNode('ParallelStmt', [p[3], p[6], p[7]])

def p_ForExp(p):
    '''ForExp : LVal ASSIGN Exp'''
    p[0] = ASTNode('ForExp', [p[1], p[3]])

# 修正后的定义
def p_PRINTFParams(p):
    '''PRINTFParams : COMMA Exp
                    | COMMA Exp PRINTFParams'''
    if len(p) == 3:
        p[0] = ASTNode('PRINTFParams', [p[2]])
    else:
        p[0] = ASTNode('PRINTFParams', [p[2]] + p[3].child_nodes)

def p_ParallelRealList(p):
    '''ParallelRealList : LVal
                        | LVal COMMA ParallelRealList'''
    if len(p) == 2:
        p[0] = ASTNode('ParallelRealList', [p[1]])
    else:
        p[0] = ASTNode('ParallelRealList', [p[1]] + p[3].child_nodes)

def p_FuncDefs(p):
    '''FuncDefs : FuncDef
                | FuncDef FuncDefs'''
    if len(p) == 2:
        # 单个函数定义
        p[0] = ASTNode('FuncDefs', [p[1]])
    else:
        # 多个函数定义
        p[0] = ASTNode('FuncDefs', [p[1]] + p[2].child_nodes)

# FuncDef (函数定义)
def p_FuncDef(p):
    '''FuncDef : DEF FuncBType IDENTIFIER LPAREN FuncFParams RPAREN  Block
               | DEF FuncBType IDENTIFIER LPAREN RPAREN Block'''
    if len(p) == 8:
        # 函数定义，有形参
        p[0] = ASTNode('FuncDef', [p[2], ASTNode('Ident', value=p[3]), p[5], p[7]])
    else:
        # 函数定义，无形参
        p[0] = ASTNode('FuncDef', [p[2], ASTNode('Ident', value=p[3]), p[6]])

# FuncFParams (函数形参列表)
def p_FuncFParams(p):
    '''FuncFParams : FuncFParam
                   | FuncFParam COMMA FuncFParams'''
    if len(p) == 2:
        p[0] = ASTNode('FuncFParams', [p[1]])
    else:
        p[0] = ASTNode('FuncFParams', [p[1]] + p[3].child_nodes)

# FuncFParam (单个形参) 可以是普通变量、一维数组或二维数组
def p_FuncFParam(p):
    '''FuncFParam : BType IDENTIFIER
                  | BType IDENTIFIER LBRACKET ConstExp RBRACKET
                  | BType IDENTIFIER LBRACKET ConstExp RBRACKET LBRACKET ConstExp RBRACKET
                  '''
    # 处理普通变量
    if len(p) == 3:
        p[0] = ASTNode('FuncFParam', [p[1], ASTNode('Ident', value=p[2])])
    # 处理一维数组
    elif len(p) == 6 and p[3] == '[' and p[5] == ']':
        p[0] = ASTNode('FuncFParam', [p[1], ASTNode('Ident', value=p[2]), p[4]])
    # 处理二维数组
    elif len(p) == 9 and p[3] == '[' and p[5] == ']' and p[6] == '[' and p[8] == ']':
        p[0] = ASTNode('FuncFParam', [p[1], ASTNode('Ident', value=p[2]), p[4], p[7]])



# FuncRParams （函数实参）
def p_FuncRParams(p):
    '''FuncRParams : Exp
                   | Exp COMMA FuncRParams'''
    if len(p) == 2:
        # 单个参数
        p[0] = ASTNode('FuncRParams', [p[1]])
    else:
        # 多个参数
        p[0] = ASTNode('FuncRParams', [p[1]] + p[3].child_nodes)

def p_Block(p):
    '''Block : LBRACE RBRACE
             | LBRACE BlockItems RBRACE
             | MUTEX IDENTIFIER LBRACE BlockItems RBRACE'''
    if len(p) == 3:
        # 空的 Block
        p[0] = ASTNode('Block', [])
    elif len(p) == 4:
        # 包含多个 BlockItem 的 Block
        p[0] = ASTNode('Block', [p[2]])
    elif len(p) == 6 and p[1] == 'mutex':
        p[0] = ASTNode('MutexBlock', [ASTNode('Ident', value=p[2]), p[4]])

def p_BlockItems(p):
    '''BlockItems : BlockItem
                  | BlockItem BlockItems'''
    if len(p) == 2:
        # 单个 BlockItem
        p[0] = ASTNode('BlockItems', [p[1]])
    else:
        # 多个 BlockItem
        p[0] = ASTNode('BlockItems', [p[1]] + p[2].child_nodes)

def p_BlockItem(p):
    '''BlockItem : Decl
                 | Stmt'''
    p[0] = ASTNode('BlockItem', [p[1]])


def p_Cond(p):
    '''Cond : LOrExp'''
    p[0] = ASTNode('Cond', [p[1]])


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
    result = f"{indent_str}ASTNode(type='{node.node_type}'"
    if node.word_value is not None:
        result += f", value='{node.word_value}'"
    if len(node.child_nodes) > 0:
        result += f", child_nodes=["

    # 递归打印子节点
    if isinstance(node.child_nodes, list) and node.child_nodes:
        child_nodes_str = []
        for child in node.child_nodes:
            child_str = format_ast(child, indent + 1)  # 子节点递归缩进
            child_nodes_str.append(child_str)
        result += "\n" + ",\n".join(child_nodes_str) + f"\n{indent_str}]"
    else:
        result += "]"  # 无子节点的情况
    result += ")"
    return result
