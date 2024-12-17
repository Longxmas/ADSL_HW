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

import re

def remove_comments(code):
    # 匹配 /* ... */ 的多行注释，并删除
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # 匹配 // ... 的单行注释，并删除
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    return code


code = """
int value1 = 0; /* vardef */
int value2 = 0; // 互斥

void main() {

  mutex a {
    x = 1;
  }
}
"""

code = remove_comments(code)
print('code = ', code)

# 词法分析
tokens = lex_input(code)
# for t in tokens:
#   print(f"{t}")

# 语法分析
result = parser.parse(code)
print(format_ast(result))
result.build()

# print(result)

generator = Generator(result)
generator.generate()
print(generator.code)
# python_code = generator.generate_code(result)
# with open('out.py', 'w') as f:
#     f.write(str(python_code))
# print(python_code)

# execute_generated_code(python_code)