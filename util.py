from typing import Optional

# 用于存储抽象语法树的工具类
class ASTNode:
    """
    parent_node: 父节点
    is_terminal: 是否是终结符
    child_nodes: is_terminal == false时才有意义，表示子节点
    word_type: is_terminal == true时才有意义，表示终结符类型（即lexer.py中的tokens）
    word_value: is_terminal == true时才有意义，表示终结符对应的值（关键字、数字、字符串）
    """
    def __init__(self,
                 parent_node: Optional['ASTNode'],
                 is_terminal: bool):
        self.parent_node = parent_node
        self.is_terminal = is_terminal
        self.child_nodes = []
        self.word_type = None
        self.word_value = None

    def set_word(self,
                 word_type: str,
                 word_value: str | int | float):
        """
        如果该节点是终结符，用该函数为word_type和word_value赋值
        """
        assert self.is_terminal == True
        self.word_type = word_type
        self.word_value = word_value

    def add_child(self, child_node: 'ASTNode'):
        """
        如果该节点是非终结符，用该函数为child_nodes添加一个子节点元素
        """
        assert self.is_terminal == False
        self.child_nodes.append(child_node)

    def __repr__(self):
        if self.is_terminal:
            return f'ASTNode(terminal, {self.word_type}, {self.word_value})'
        else:
            return f"ASTNode(nonterminal, child_nodes={self.child_nodes})"

# 测试
if __name__ == '__main__':
    root_node = ASTNode(None, False)
    child1 = ASTNode(root_node, True)
    child2 = ASTNode(root_node, True)
    root_node.add_child(child1)
    root_node.add_child(child2)
    print(root_node)