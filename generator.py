from util import ASTNode

class Generator:
    def __init__(self, root_node: ASTNode):
        self.root_node = root_node
        self.code = ""
        self.temp_code = ""     # 备份code
        self.parallel_code = ""
        self.parallel_cnt = 0

    def generate(self):
        assert equals_NT(self.root_node, 'CompUnit')
        self.g_CompUnit(self.root_node)
        self.code += self.parallel_code

    def g_CompUnit(self, node: ASTNode):
        self.code += 'package main\nimport \"fmt\"\n'
        for child in node.child_nodes:
            if equals_NT(child, 'Decls'):
                self.g_Decls(child)
            elif equals_NT(child, 'FuncDefs'):
                self.g_FuncDefs(child)
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
        # 需要将btype传入子函数
        children = node.child_nodes
        assert equals_T(children[0], 'BType')
        btype = children[0]
        assert equals_NT(children[1], 'ConstDefList')
        self.g_ConstDefList(children[1], btype)

    def g_ConstDefList(self, node: ASTNode, btype):
        for child in node.child_nodes:
            if equals_NT(child, 'ConstDef'):
                self.g_ConstDef(child, btype)
            else:
                raise RuntimeError("g_ConstDefList fail")

    def g_ConstDef(self, node: ASTNode, btype):
        children = node.child_nodes
        self.g_CONST()
        self.g_SPACE()
        assert equals_T(children[0], 'Ident')
        self.g_Ident(children[0])
        self.g_SPACE()
        if self.get_type_prefix(btype) is not None:
            raise RuntimeError("mutex/pipe cannot be const")
        if len(children) == 2:      # 非数组
            self.g_BType(btype)
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_ConstInitVal(children[1])
        elif len(children) == 3:    # 一维数组
            self.g_LBRACKET()
            self.g_ConstExp(children[1])
            self.g_RBRACKET()
            self.g_BType(btype)
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_LBRACKET()
            self.g_ConstExp(children[1])
            self.g_RBRACKET()
            self.g_BType(btype)
            self.g_ConstInitVal(children[2])
        elif len(children) == 4:    # 二维数组
            self.g_LBRACKET()
            self.g_ConstExp(children[1])
            self.g_RBRACKET()
            self.g_LBRACKET()
            self.g_ConstExp(children[2])
            self.g_RBRACKET()
            self.g_BType(btype)
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_LBRACKET()
            self.g_ConstExp(children[1])
            self.g_RBRACKET()
            self.g_LBRACKET()
            self.g_ConstExp(children[2])
            self.g_RBRACKET()
            self.g_BType(btype)
            self.g_ConstInitVal(children[3])
        else:
            raise RuntimeError("g_ConstDef fail")
        self.g_NEWLINE()

    def g_ConstInitVal(self, node: ASTNode):
        if equals_NT(node.child_nodes[0], 'ConstExp'):
            self.g_ConstExp(node.child_nodes[0])
        elif equals_NT(node.child_nodes[0], 'ConstInitValList'):
            self.g_LBRACE()
            self.g_ConstInitValList(node.child_nodes[0])
            self.g_RBRACE()
        else:
            raise RuntimeError("g_ConstInitVal fail")

    def g_ConstInitValList(self, node: ASTNode):
        for index, child in enumerate(node.child_nodes):
            if equals_NT(child, 'ConstInitVal'):
                self.g_ConstInitVal(child)
                if index < len(node.child_nodes) - 1:
                    self.g_COMMA()
                    self.g_SPACE()
            else:
                raise RuntimeError("g_ConstInitValList fail")

    def g_ConstExp(self, node: ASTNode):
        assert equals_NT(node.child_nodes[0], 'AddExp')
        self.g_AddExp(node.child_nodes[0])

    def g_VarDecl(self, node: ASTNode):
        children = node.child_nodes
        assert equals_T(children[0], 'BType')
        btype = children[0]
        assert equals_NT(children[1], 'VarDefList')
        self.g_VarDefList(children[1], btype)

    def g_VarDefList(self, node: ASTNode, btype):
        for child in node.child_nodes:
            if equals_NT(child, 'VarDef'):
                self.g_VarDef(child, btype)
            else:
                raise RuntimeError("g_VarDefList fail")

    def g_VarDef(self, node: ASTNode, btype):
        children = node.child_nodes
        self.g_VAR()
        self.g_SPACE()
        assert equals_T(children[0], 'Ident')
        ident = children[0]
        self.g_Ident(ident)
        self.g_SPACE()
        if len(children) == 1:      # int x
            if self.get_type_prefix(btype) == 'pipe':
                self.g_CHAN()
                self.g_SPACE()
                self.g_BType(btype)
                self.g_SPACE()
                self.g_ASSIGN()
                self.g_SPACE()
                self.g_MAKE()
                self.g_LPAREN()
                self.g_CHAN()
                self.g_SPACE()
                self.g_BType(btype)
                self.g_RPAREN()
            else:
                self.g_BType(btype)
        elif len(children) == 3:    # int x[a][b] = c
            self.g_ArrayDimensions(children[1])
            self.g_BType(btype)
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_ArrayDimensions(children[1])
            self.g_BType(btype)
            self.g_InitVal(children[2])
        elif equals_NT(children[1], 'ArrayDimensions'): # int x[a][b]
            array_dim = children[1]
            self.g_ArrayDimensions(array_dim)
            if self.get_type_prefix(btype) == 'pipe':
                self.g_CHAN()
                self.g_SPACE()
                self.g_BType(btype)
                self.g_NEWLINE()
                # use for to make chan
                if len(array_dim.child_nodes) == 1: # 一维
                    self.code += "for _i := 0; _i < "
                    self.g_ConstExp(array_dim.child_nodes[0])
                    self.code += "; _i++ { "
                    self.g_Ident(ident)
                    self.code += "[_i] = make(chan "
                    self.g_BType(btype)
                    self.code += ") }"
                else:   # 二维
                    self.code += "for _i := 0; _i < "
                    self.g_ConstExp(array_dim.child_nodes[0])
                    self.code += "; _i++ { for _j := 0; _j < "
                    self.g_ConstExp(array_dim.child_nodes[1])
                    self.code += "; _j++ { "
                    self.g_Ident(ident)
                    self.code += "[_i][_j] = make(chan "
                    self.g_BType(btype)
                    self.code += ") }}"
            else:
                self.g_BType(btype)
        elif equals_NT(children[1], 'InitVal'): # int x = c
            self.g_BType(btype)
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_InitVal(children[1])
        else:
            raise RuntimeError("g_VarDef fail")
        self.g_NEWLINE()

    def g_ArrayDimensions(self, node: ASTNode):
        for child in node.child_nodes:
            assert equals_NT(child, 'ConstExp')
            self.g_LBRACKET()
            self.g_ConstExp(child)
            self.g_RBRACKET()

    def g_InitVal(self, node: ASTNode):
        if equals_NT(node.child_nodes[0], 'Exp'):
            self.g_Exp(node.child_nodes[0])
        elif equals_NT(node.child_nodes[0], 'InitValList'):
            self.g_LBRACE()
            self.g_InitValList(node.child_nodes[0])
            self.g_RBRACE()
        else:
            raise RuntimeError("g_InitVal fail")

    def g_InitValList(self, node: ASTNode):
        for index, child in enumerate(node.child_nodes):
            if equals_NT(child, 'InitVal'):
                self.g_InitVal(child)
                if index < len(node.child_nodes) - 1:
                    self.g_COMMA()
                    self.g_SPACE()
            else:
                raise RuntimeError("g_InitValList fail")

    def g_Exp(self, node: ASTNode):
        assert equals_NT(node.child_nodes[0], 'AddExp')
        self.g_AddExp(node.child_nodes[0])

    def g_LOrExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'LAndExp'):
            self.g_LAndExp(children[0])
        elif equals_NT(children[0], 'LOrExp'):
            self.g_LOrExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_LAndExp(children[2])
        else:
            raise RuntimeError("g_LOrExp fail")

    def g_LAndExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'EqExp'):
            self.g_EqExp(children[0])
        elif equals_NT(children[0], 'LAndExp'):
            self.g_LAndExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_EqExp(children[2])
        else:
            raise RuntimeError("g_LAndExp fail")

    def g_AddExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'MulExp'):
            self.g_MulExp(children[0])
        elif equals_NT(children[0], 'AddExp'):
            self.g_AddExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_MulExp(children[2])
        else:
            raise RuntimeError("g_AddExp fail")

    def g_MulExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'UnaryExp'):
            self.g_UnaryExp(children[0])
        elif equals_NT(children[0], 'MulExp'):
            self.g_MulExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_UnaryExp(children[2])
        else:
            raise RuntimeError("g_MulExp fail")

    def g_EqExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'RelExp'):
            self.g_RelExp(children[0])
        elif equals_NT(children[0], 'EqExp'):
            self.g_EqExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_RelExp(children[2])
        else:
            raise RuntimeError("g_EqExp fail")

    def g_RelExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'AddExp'):
            self.g_AddExp(children[0])
        elif equals_NT(children[0], 'RelExp'):
            self.g_RelExp(children[0])
            self.g_SPACE()
            self.g_Op(children[1])
            self.g_SPACE()
            self.g_AddExp(children[2])
        else:
            raise RuntimeError("g_RelExp fail")

    def g_UnaryExp(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(children[0], 'PrimaryExp'):
            self.g_PrimaryExp(children[0])
        elif equals_T(children[0], 'Ident'):
            self.g_Ident(children[0])
            self.g_LPAREN()
            self.g_FuncRParams(children[1])
            self.g_RPAREN()
        elif equals_T(children[0], 'UnaryOp'):
            self.g_UnaryOp(children[0])
            self.g_UnaryExp(children[1])
        else:
            raise RuntimeError("g_UnaryExp fail")

    def g_PrimaryExp(self, node: ASTNode):
        if equals_NT(node.child_nodes[0], 'Exp'):
            self.g_LPAREN()
            self.g_Exp(node.child_nodes[0])
            self.g_RPAREN()
        elif equals_NT(node.child_nodes[0], 'LVal'):
            self.g_LVal(node.child_nodes[0])
        elif equals_T(node.child_nodes[0], 'IntConst'):
            self.g_INTCONST(node.child_nodes[0])
        elif equals_T(node.child_nodes[0], 'FloatConst'):
            self.g_FLOATCONST(node.child_nodes[0])
        elif equals_T(node.child_nodes[0], 'STRCONST'):
            self.g_STRCONST(node.child_nodes[0])
        elif equals_NT(node.child_nodes[0], 'BoolConst'):
            self.g_BoolConst(node.child_nodes[0])
        else:
            raise RuntimeError("g_PrimaryExp fail")

    def g_LVal(self, node: ASTNode):
        assert equals_T(node.child_nodes[0], 'Ident')
        self.g_Ident(node.child_nodes[0])
        if len(node.child_nodes) == 2:
            assert equals_NT(node.child_nodes[1], 'ArrayDimensions')
            self.g_ArrayDimensions(node.child_nodes[1])

    def g_MainFuncDef(self, node: ASTNode):
        self.g_FUNC()
        self.g_SPACE()
        self.g_MAIN()
        self.g_LPAREN()
        self.g_RPAREN()
        self.g_SPACE()
        assert equals_NT(node.child_nodes[0], 'Block')
        self.g_Block(node.child_nodes[0])

    def g_Stmt(self, node: ASTNode):
        children = node.child_nodes
        if equals_NT(node, 'AssignStmt'):
            self.g_LVal(children[0])
            self.g_SPACE()
            self.g_ASSIGN()
            self.g_SPACE()
            self.g_Exp(children[1])
            self.g_NEWLINE()
        elif equals_NT(node, 'ShiftLeftStmt'):
            self.g_Exp(children[0])
            self.g_SPACE()
            self.g_LSHIFT()
            self.g_SPACE()
            self.g_Exp(children[1])
            self.g_NEWLINE()
        elif equals_NT(node, 'ShiftRightStmt'):
            self.g_Exp(children[1])
            self.g_SPACE()
            self.g_RSHIFT()
            self.g_SPACE()
            self.g_Exp(children[0])
            self.g_NEWLINE()
        elif equals_NT(node, 'ExpStmt'):
            self.g_Exp(children[0])
            self.g_NEWLINE()
        elif equals_NT(node, 'EmptyStmt'):
            self.g_NEWLINE()
        elif equals_NT(node, 'BlockStmt'):
            self.g_Block(children[0])
        elif equals_NT(node, 'IfStmt'):
            self.g_IF()
            self.g_SPACE()
            self.g_Cond(children[0])
            self.g_SPACE()
            self.g_Stmt(children[1])
            if len(children) == 3:
                self.g_ELSE()
                self.g_SPACE()
                self.g_Stmt(children[2])
        elif equals_NT(node, 'ForStmt'):
            self.g_FOR()
            self.g_SPACE()
            if equals_T(children[0], 'Ident'):  # for _, i := range arr
                self.g_UNDERLINE()
                self.g_COMMA()
                self.g_SPACE()
                self.g_Ident(children[0])
                self.g_SPACE()
                self.g_INFER_ASSIGN()
                self.g_SPACE()
                self.g_RANGE()
                self.g_SPACE()
                self.g_Ident(children[1])
                self.g_SPACE()
                self.g_Stmt(children[2])
            else:   # for ;;
                if len(children) == 4:      # for x;x;x
                    assert equals_NT(children[0], 'ForExp')
                    self.g_ForExp(children[0])
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    assert equals_NT(children[1], 'Cond')
                    self.g_Cond(children[1])
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    assert equals_NT(children[2], 'ForExp')
                    self.g_ForExp(children[2])
                    self.g_SPACE()
                    self.g_Stmt(children[3])
                elif equals_NT(children[0], 'Cond'):    # for ;x;x
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    assert equals_NT(children[0], 'Cond')
                    self.g_Cond(children[0])
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    assert equals_NT(children[1], 'ForExp')
                    self.g_ForExp(children[1])
                    self.g_SPACE()
                    self.g_Stmt(children[2])
                elif equals_NT(children[1], 'Cond'):    # for x;x;
                    assert equals_NT(children[0], 'ForExp')
                    self.g_ForExp(children[0])
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    self.g_Cond(children[1])
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    self.g_Stmt(children[2])
                else:       # for x;;x
                    assert equals_NT(children[0], 'ForExp')
                    self.g_ForExp(children[0])
                    self.g_SEMICOLON()
                    self.g_SEMICOLON()
                    self.g_SPACE()
                    assert equals_NT(children[1], 'ForExp')
                    self.g_ForExp(children[1])
                    self.g_SPACE()
                    self.g_Stmt(children[2])
        elif equals_NT(node, 'BreakStmt'):
            self.g_BREAK()
            self.g_NEWLINE()
        elif equals_NT(node, 'ContinueStmt'):
            self.g_CONTINUE()
            self.g_NEWLINE()
        elif equals_NT(node, 'ReturnStmt'):
            self.g_RETURN()
            if len(children) == 1:
                self.g_SPACE()
                self.g_Exp(children[0])
            self.g_NEWLINE()
        elif equals_NT(node, 'GetIntStmt'):
            self.code += r'fmt.Scanf("%d", &'
            self.g_LVal(children[0])
            self.code += ')'
        elif equals_NT(node, 'PrintfStmt'):
            self.code += 'fmt.Printf'
            self.g_LPAREN()
            self.g_STRCONST(children[0])
            if len(children) == 2:
                self.g_PRINTFParams(children[1])
            self.g_RPAREN()
            self.g_NEWLINE()
        elif equals_NT(node, 'ParallelStmt'):
            # 生成parallel_code
            self.temp_code = self.code
            self.code = ""
            self.code += f"func parallel_{self.parallel_cnt} ("
            assert equals_NT(children[0], 'FuncFParams')
            self.g_FuncFParams(children[0])
            self.code += ")"
            assert equals_NT(children[2], 'Block')
            self.g_Block(children[2])
            self.parallel_code += self.code
            self.code = self.temp_code
            # 生成code
            self.code += f"for _i := 0; _i < len("
            self.code += f"go parallel_{self.parallel_cnt}("
            self.g_FuncRParams()
            self.parallel_cnt += 1
        else:
            raise RuntimeError("g_Stmt fail")

    def g_ForExp(self, node: ASTNode):
        children = node.child_nodes
        assert equals_NT(children[0], 'LVal')
        self.g_LVal(children[0])
        self.g_SPACE()
        self.g_ASSIGN()
        self.g_SPACE()
        assert equals_NT(children[1], 'Exp')
        self.g_Exp(children[1])

    def g_PRINTFParams(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'Exp'):
                self.g_COMMA()
                self.g_SPACE()
                self.g_Exp(child)
            else:
                raise RuntimeError("g_PRINTFParams fail")

    def g_FuncDefs(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'FuncDef'):
                self.g_FuncDef(child)
            else:
                raise RuntimeError("g_FuncDefs fail")

    def g_FuncDef(self, node: ASTNode):
        children = node.child_nodes
        self.g_FUNC()
        self.g_SPACE()
        assert equals_T(children[0], 'BType')
        assert equals_T(children[1], 'Ident')
        self.g_Ident(children[1])
        self.g_LPAREN()
        if equals_NT(children[2], 'FuncFParams'):
            self.g_FuncFParams(children[2])
        self.g_RPAREN()
        self.g_SPACE()
        self.g_BType(children[0])
        self.g_SPACE()
        if equals_NT(children[2], 'Block'):
            self.g_Block(children[2])
        else:
            self.g_Block(children[3])

    def g_FuncFParams(self, node: ASTNode):
        for index, child in enumerate(node.child_nodes):
            if equals_NT(child, 'FuncFParam'):
                self.g_FuncFParam(child)
                if index < len(node.child_nodes) - 1:
                    self.g_COMMA()
                    self.g_SPACE()
            else:
                raise RuntimeError("g_FuncFParams fail")

    def g_FuncFParam(self, node: ASTNode):
        assert equals_T(node.child_nodes[1], 'Ident')
        self.g_Ident(node.child_nodes[1])
        self.g_SPACE()
        assert equals_T(node.child_nodes[0], 'BType')
        self.g_BType(node.child_nodes[0])

    def g_FuncRParams(self, node: ASTNode):
        for index, child in enumerate(node.child_nodes):
            if equals_NT(child, 'Exp'):
                self.g_Exp(child)
                if index < len(node.child_nodes) - 1:
                    self.g_COMMA()
                    self.g_SPACE()
            else:
                raise RuntimeError("g_FuncRParams fail")

    def g_Block(self, node: ASTNode):
        self.g_LBRACE()
        self.g_NEWLINE()
        if equals_NT(node.child_nodes[0], 'BlockItems'):
            self.g_BlockItems(node.child_nodes[0])
        self.g_RBRACE()
        self.g_NEWLINE()

    def g_BlockItems(self, node: ASTNode):
        for child in node.child_nodes:
            if equals_NT(child, 'BlockItem'):
                self.g_BlockItem(child)
            else:
                raise RuntimeError("g_BlockItems fail")

    def g_BlockItem(self, node: ASTNode):
        if equals_NT(node.child_nodes[0], 'Decl'):
            self.g_Decl(node.child_nodes[0])
        else:
            assert node.child_nodes[0].node_type.endswith('Stmt')
            self.g_Stmt(node.child_nodes[0])

    def g_Cond(self, node: ASTNode):
        assert equals_NT(node.child_nodes[0], 'LOrExp')
        self.g_LOrExp(node.child_nodes[0])

    ################################################################
    # 以下是终结符
    ################################################################
    def g_BType(self, node: ASTNode):
        self.code += node.word_value.split(' ')[-1]
    def get_type_prefix(self, node: ASTNode):
        values = node.word_value.split(' ')
        if len(values) == 1:
            return None
        else:
            return values[0]
    def g_Op(self, node: ASTNode):
        self.code += node.word_value
    def g_UnaryOp(self, node: ASTNode):
        self.code += node.word_value
    def g_Ident(self, node: ASTNode):
        self.code += node.word_value
    def g_INTCONST(self, node: ASTNode):
        self.code += str(node.word_value)
    def g_FLOATCONST(self, node: ASTNode):
        self.code += str(node.word_value)
    def g_STRCONST(self, node: ASTNode):
        self.code += f'\"{repr(node.word_value)[1:-1]}\"'
    def g_BoolConst(self, node: ASTNode):
        self.code += node.word_value
    def g_TRUE(self):
        self.code += 'true'
    def g_FALSE(self):
        self.code += 'false'

    def g_NEWLINE(self):
        self.code += '\n'
    def g_SPACE(self):
        self.code += ' '
    def g_UNDERLINE(self):
        self.code += '_'
    def g_SEMICOLON(self):
        self.code += ';'
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
        self.code += '<-'
    def g_RSHIFT(self):
        self.code += '= <-'
    def g_INFER_ASSIGN(self):
        self.code += ':='

    def g_FUNC(self):
        self.code += 'func'
    def g_MAIN(self):
        self.code += 'main'
    def g_IF(self):
        self.code += 'if'
    def g_ELSE(self):
        self.code += 'else'
    def g_FOR(self):
        self.code += 'for'
    def g_BREAK(self):
        self.code += 'break'
    def g_CONTINUE(self):
        self.code += 'continue'
    def g_RETURN(self):
        self.code += 'return'
    def g_RANGE(self):
        self.code += 'range'
    def g_PARALLEL(self):
        self.code += 'parallel'
    def g_CONST(self):
        self.code += 'const'
    def g_VAR(self):
        self.code += 'var'
    def g_CHAN(self):
        self.code += 'chan'
    def g_MAKE(self):
        self.code += 'make'



# 是否是某个终结符
def equals_T(node: ASTNode, word: str) -> bool:
    return node.is_terminal and node.word_type == word
# 是否是某个非终结符
def equals_NT(node: ASTNode, name: str) -> bool:
    return not node.is_terminal and node.node_type == name