from util import ASTNode

class Generator:
    SEP = '\n'      # 分隔符

    def __init__(self, root_node: ASTNode):
        self.root_node = root_node
        self.code = ""

    def generate(self):
        assert (self.root_node.is_terminal == False and
                self.root_node.node_type == 'CompUnit')
        self.g_CompUnit(self.root_node)

    def g_CompUnit(self, node: ASTNode):
        self.code += 'package main\nimport \"fmt\"\n'
        for child in node.child_nodes:
            if equals_NT(child, 'Decls'):
                self.g_Decls(child)
            elif equals_NT(child, 'FuncDefs'):
                self.p_FuncDefs(child)
            elif equals_NT(child, 'MainFuncDef'):
                self.g_MainFuncDef(child)
            else:
                raise RuntimeError("g_CompUnit fail")

    def g_Decls(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'Decl'):
                self.g_Decl(child)
            else:
                raise RuntimeError("g_Decls fail")

    def g_Decl(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'ConstDecl'):
                self.g_ConstDecl(child)
            elif equals_NT(child, 'VarDecl'):
                self.g_VarDecl(child)
            else:
                raise RuntimeError("g_Decl fail")

    def g_ConstDecl(self, node: ASTNode):
        # TODO
        children = node.child_nodes
        self.g_CONST()
        assert equals_NT(children[0], 'BType')
        self.g_BType(children[0])
        assert equals_NT(children[1], 'ConstDefList')
        self.g_ConstDefList(children[1])
        self.g_SEMICOLON()

    def g_ConstDefList(self, node: ASTNode):
        # TODO
        for child in node.child_nodes:
            if equals_NT(child, 'ConstDef'):
                self.g_ConstDef(child)
            elif equals_T(child, 'COMMA'):
                self.g_COMMA()
            elif equals_NT(child, 'ConstDefList'):
                self.g_ConstDefList(child)
            else:
                raise RuntimeError("g_ConstDefList fail")

    def g_ConstDef(self, node: ASTNode):
        # TODO
        for child in node.child_nodes:
            if equals_T(child, 'IDENTIFIER'):
                self.g_IDENTIFIER(child)
            elif equals_T(child, 'LBRACKET'):
                self.g_LBRACKET()
            elif equals_T(child, 'RBRACKET'):
                self.g_RBRACKET()
            elif equals_NT(child, 'ConstExp'):
                self.g_ConstExp(child)
            elif equals_T(child, 'ASSIGN'):
                self.g_ASSIGN()
            elif equals_NT(child, 'ConstInitVal'):
                self.g_ConstInitVal(child)
            else:
                raise RuntimeError("g_ConstDef fail")

    def g_ConstInitVal(self, node: ASTNode):
        # TODO
        for child in node.child_nodes:
            if equals_NT(child, 'ConstExp'):
                self.g_ConstExp(child)
            elif equals_T(child, 'LBRACE'):
                self.g_LBRACE()
            elif equals_T(child, 'RBRACE'):
                self.g_RBRACE()
            elif equals_NT(child, 'ConstInitValList'):
                self.g_ConstInitValList(child)
            else:
                raise RuntimeError("g_ConstInitVal fail")

    def g_ConstInitValList(self, node: ASTNode):
        # TODO
        for child in node.child_nodes:
            if equals_NT(child, 'ConstInitVal'):
                self.g_ConstInitVal(child)
            elif equals_T(child, 'COMMA'):
                self.g_COMMA()
            elif equals_NT(child, 'ConstInitValList'):
                self.g_ConstInitValList(child)
            else:
                raise RuntimeError("g_ConstInitValList fail")

    def g_ConstExp(self, node: ASTNode):
        # TODO
        for child in node.child_nodes:
            if equals_NT(child, 'AddExp'):
                self.g_AddExp(child)
            else:
                raise RuntimeError("g_ConstExp fail")

    def g_BType(self, node: ASTNode):
        # TODO
        pass

    def g_Exp(self, node: ASTNode):
        self.g_AddExp(node.child_nodes[0])

    def g_LOrExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'LAndExp'):
                self.g_LAndExp(child)
            elif equals_NT(child, 'LOrExp'):
                self.g_LOrExp(child)
            elif equals_T(child, 'LOGICALOR'):
                self.g_LOGICALOR()
            else:
                raise RuntimeError("g_LOrExp fail")

    def g_LAndExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'EqExp'):
                self.g_EqExp(child)
            elif equals_NT(child, 'LAndExp'):
                self.g_LAndExp(child)
            elif equals_T(child, 'LOGICALAND'):
                self.g_LOGICALAND()
            else:
                raise RuntimeError("g_LAndExp fail")

    def g_AddExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'MulExp'):
                self.g_MulExp(child)
            elif equals_NT(child, 'AddExp'):
                self.g_AddExp(child)
            elif equals_T(child, 'PLUS'):
                self.g_PLUS()
            elif equals_T(child, 'MINUS'):
                self.g_MINUS()
            else:
                raise RuntimeError("g_AddExp fail")

    def g_MulExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'UnaryExp'):
                self.g_UnaryExp(child)
            elif equals_T(child, 'MulExp'):
                self.g_MulExp(child)
            elif equals_T(child, 'TIMES'):
                self.g_TIMES()
            elif equals_T(child, 'DIVIDE'):
                self.g_DIVIDE()
            elif equals_T(child, 'MOD'):
                self.g_MOD()
            else:
                raise RuntimeError("g_MulExp fail")

    def g_EqExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'RelExp'):
                self.g_RelExp(child)
            elif equals_NT(child, 'EqExp'):
                self.g_EqExp(child)
            elif equals_T(child, 'EQUAL'):
                self.g_EQUAL()
            elif equals_T(child, 'NOTEQUAL'):
                self.g_NOTEQUAL()
            else:
                raise RuntimeError("g_EqExp fail")

    def g_RelExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'AddExp'):
                self.g_AddExp(child)
            elif equals_NT(child, 'RelExp'):
                self.g_RelExp(child)
            elif equals_T(child, 'LESS'):
                self.g_LESS()
            elif equals_T(child, 'LESSEQUAL'):
                self.g_LESSEQUAL()
            elif equals_T(child, 'GREATER'):
                self.g_GREATER()
            elif equals_T(child, 'GREATEREQUAL'):
                self.g_GREATEREQUAL()
            else:
                raise RuntimeError("g_RelExp fail")

    def g_UnaryExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'PrimaryExp'):
                self.g_PrimaryExp(child)
            elif equals_T(child, 'IDENTIFIER'):
                self.g_IDENTIFIER()
            elif equals_T(child, 'LPAREN'):
                self.g_LPAREN()
            elif equals_T(child, 'RPAREN'):
                self.g_RPAREN()
            elif equals_NT(child, 'FuncRParams'):
                self.g_FuncRParams(child)
            elif equals_NT(child, 'UnaryOp'):
                self.g_UnaryOp(child)
            elif equals_NT(child, 'UnaryExp'):
                self.g_UnaryExp(child)
            else:
                raise RuntimeError("g_UnaryExp fail")

    def g_UnaryOp(self, node: ASTNode):
        child = node.child_nodes[0]
        if equals_T(child, 'PLUS'):
            self.g_PLUS()
        elif equals_T(child, 'MINUS'):
            self.g_MINUS()
        elif equals_T(child, 'NOT'):
            self.g_NOT()
        else:
            raise RuntimeError("g_UnaryOp fail")

    def g_PrimaryExp(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_T(child, 'LPAREN'):
                self.g_LPAREN()
            elif equals_T(child, 'RPAREN'):
                self.g_RPAREN()
            elif equals_NT(child, 'Exp'):
                self.g_Exp(child)
            elif equals_NT(child, 'LVal'):
                self.g_LVal(child)
            elif equals_T(child, 'INTCONST'):
                self.g_INTCONST()
            elif equals_T(child, 'FLOATCONST'):
                self.g_FLOATCONST()
            elif equals_T(child, 'STRCONST'):
                self.g_STRCONST()
            elif equals_T(child, 'TRUE'):
                self.g_TRUE()
            elif equals_T(child, 'FALSE'):
                self.g_FALSE()
            else:
                raise RuntimeError("g_PrimaryExp fail")

    def g_LVal(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_T(child, 'IDENTIFIER'):
                self.g_IDENTIFIER(child)
            elif equals_NT(child, 'ArrayDimensions'):
                self.g_ArrayDimensions(child)
            else:
                raise RuntimeError("g_LVal fail")

    def g_MainFuncDef(self, node: ASTNode):
        self.g_FUNC()
        self.g_MAIN()
        self.g_LPAREN()
        self.g_RPAREN()
        assert equals_NT(node.child_nodes[0], 'Block')
        self.g_Block(node.child_nodes[0])

    def g_Stmt(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'Exp'):
            self.g_Exp(children[0])
            self.g_SEMICOLON()
        elif equals_T(children[0], 'SEMICOLON'):
            self.g_SEMICOLON()
        elif equals_NT(children[0], 'Block'):
            self.g_Block(children[0])
        elif equals_T(children[0], 'IF'):
            self.g_IF()
            self.g_LPAREN()
            self.g_Cond()
            self.g_RPAREN()
            self.g_Stmt(children[4])
            if len(children) == 7:
                self.g_ELSE()
                self.g_Stmt(children[6])
        elif equals_T(children[0], 'FOR'):
            # TODO
            pass
        elif equals_T(children[0], 'BREAK'):
            self.g_BREAK()
            self.g_SEMICOLON()
        elif equals_T(children[0], 'CONTINUE'):
            self.g_CONTINUE()
            self.g_SEMICOLON()
        elif equals_T(children[0], 'RETURN'):
            self.g_RETURN()
            if len(children) == 3:
                self.g_Exp(children[1])
            self.g_SEMICOLON()
        elif equals_NT(children[0], 'LVal'):
            if equals_T(children[1], 'LSHIFT'):
                self.g_LVal(children[0])
                self.g_LSHIFT()
                self.g_LVal(children[2])
            elif equals_T(children[2], 'GETINT'):
                self.code += 'fmt.Scanf(\"%d\", &'
                self.g_LVal(children[0])
                self.code += ')'
            else:
                self.g_LVal(children[0])
                self.g_ASSIGN()
                self.g_Exp(children[2])
            self.g_SEMICOLON()
        elif equals_T(children[0], 'PRINTF'):
            self.code += 'fmt.Printf'
            self.g_LPAREN()
            self.g_STRCONST(children[2])
            if equals_NT(children[3], 'PRINTFParams'):
                self.g_PRINTFParams(children[3])
            self.g_RPAREN()
            self.g_SEMICOLON()
        elif equals_T(children[0], 'PARALLEL'):
            pass
        else:
            raise RuntimeError("g_Stmt fail")

    def g_PRINTFParams(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'Exp'):
                self.g_COMMA()
                self.g_Exp(child)
            else:
                raise RuntimeError("g_PRINTFParams fail")

    def g_FuncDefs(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'FuncDef'):
                self.g_FuncDef()
            else:
                raise RuntimeError("g_FuncDefs fail")

    def g_FuncDef(self, node: ASTNode):
        self.g_FUNC()
    ################################################################
    # 以下是终结符
    ################################################################
    def g_IDENTIFIER(self, node: ASTNode):
        self.code += node.word_value
    def g_INTCONST(self, node: ASTNode):
        self.code += str(node.word_value)
    def g_FLOATCONST(self, node: ASTNode):
        self.code += str(node.word_value)
    def g_STRCONST(self, node: ASTNode):
        self.code += node.word_value
    def g_TRUE(self):
        self.code += 'true'
    def g_FALSE(self):
        self.code += 'false'

    def g_SEMICOLON(self):
        self.code += Generator.SEP
    def g_COMMA(self):
        self.code += ','
    def g_LPAREN(self):
        self.code += '('
    def g_RPAREN(self):
        self.code += ')'
    def g_LBRACKET(self):
        self.code += '['
    def g_RBRACKET(self):
        self.code += ']'
    def g_LBRACE(self):
        self.code += '{'
    def g_RBRACE(self):
        self.code += '}'
    def g_ASSIGN(self):
        self.code += '='
    def g_PLUS(self):
        self.code += '+'
    def g_MINUS(self):
        self.code += '-'
    def g_TIMES(self):
        self.code += '*'
    def g_DIVIDE(self):
        self.code += '/'
    def g_MOD(self):
        self.code += '%'
    def g_EQUAL(self):
        self.code += '=='
    def g_NOTEQUAL(self):
        self.code += '!='
    def g_LESS(self):
        self.code += '<'
    def g_LESSEQUAL(self):
        self.code += '<='
    def g_GREATER(self):
        self.code += '>'
    def g_GREATEREQUAL(self):
        self.code += '>='
    def g_LOGICALOR(self):
        self.code += '||'
    def g_LOGICALAND(self):
        self.code += '&&'
    def g_NOT(self):
        self.code += '!'
    def g_LSHIFT(self):
        self.code += '<<'

    def g_FUNC(self):
        self.code += 'func '
    def g_MAIN(self):
        self.code += 'main'
    def g_IF(self):
        self.code += 'if'
    def g_ELSE(self):
        self.code += 'else'
    def g_FOR(self):
        self.code += 'for '
    def g_IN(self):
        self.code += 'in '
    def g_BREAK(self):
        self.code += 'break'
    def g_CONTINUE(self):
        self.code += 'continue'
    def g_RETURN(self):
        self.code += 'return'
    def g_CONST(self):
        self.code += 'const '
    def g_INT(self):
        self.code += 'int '



# 是否是某个终结符
def equals_T(node: ASTNode, word: str) -> bool:
    return node.is_terminal and node.word_type == word
# 是否是某个非终结符
def equals_NT(node: ASTNode, name: str) -> bool:
    return not node.is_terminal and node.node_type == name