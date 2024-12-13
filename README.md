自定义语言

核心特点：parallel(list) {... return x}就会把list里面的每一个元素当作参数，创建len(list)个线程并行执行，执行完把每个线程的返回值包装成数组再返回
翻译为python

利用ply实现词法与文法分析

## 词法分析 
lexer

## 语法分析
parser

## 代码生成
generator

### 示例

假设有以下代码：

```
parallel(x in [1, 2, 3]) {
  x = x * 2;
  return x;
}
```

1. **词法分析** 
Tokens: [LexToken(PARALLEL,'parallel',1,1), LexToken(LPAREN,'(',1,9), LexToken(IDENTIFIER,'x',1,10), LexToken(IN,'in',1,12), LexToken(LBRACKET,'[',1,15), LexToken(NUMBER,'1',1,16), LexToken(COMMA,',',1,17), LexToken(NUMBER,'2',1,19), LexToken(COMMA,',',1,20), LexToken(NUMBER,'3',1,22), LexToken(RBRACKET,']',1,23), LexToken(RPAREN,')',1,24), LexToken(LBRACE,'{',1,26), LexToken(IDENTIFIER,'x',1,30), LexToken(EQUALS,'=',1,32), LexToken(IDENTIFIER,'x',1,34), LexToken(TIMES,'*',1,36), LexToken(NUMBER,'2',1,38), LexToken(SEMICOLON,';',1,39), LexToken(RETURN,'return',1,43), LexToken(IDENTIFIER,'x',1,50), LexToken(SEMICOLON,';',1,51), LexToken(RBRACE,'}',1,53)]
2. **语法分析** 
```
{'type': 'parallel', 'variable': 'x', 'list': [1, 2, 3], 'body': [{'type': 'assign', 'variable': 'x', 'expr': {'type': 'multiply', 'left': 'x', 'right': '2'}}, {'type': 'return', 'value': 'x'}]}
```
3. **代码生成**
```
from concurrent.futures import ThreadPoolExecutor
def compute(x):
    x = x * 2
    return x
result = list(ThreadPoolExecutor().map(compute, [1, 2, 3]))
```