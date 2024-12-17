import os

from lexer import lexer, lex_input
from parser import parser, format_ast
from generator import Generator
import re

def execute_generated_code(generated_code):
    local_vars = {}
    exec(generated_code, {}, local_vars)
    result = local_vars.get('result', [])
    with open('output.txt', 'w') as f:
        f.write(str(result))

def remove_comments(code):
    # 匹配 /* ... */ 的多行注释，并删除
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # 匹配 // ... 的单行注释，并删除
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    return code


code = ""
with open("testcase/full.c", 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        code += line
        line = f.readline()

code = remove_comments(code)
# print('code = ', code)

# 词法分析
tokens = lex_input(code)
# for t in tokens:
#   print(f"{t}")
print("词法分析成功")

# 语法分析
result = parser.parse(code)
# print(format_ast(result))
result.build()
print("语法分析成功")

# print(result)

generator = Generator(result)
generator.generate()
# print(generator.code)
with open("code_output.go", "w", encoding='utf-8') as f:
    f.write(generator.code)
print("代码生成成功")

print("运行程序 >>> go run code_output.go")
output = os.popen("go run code_output.go").read()
print(output)