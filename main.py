from lexer import lexer, lex_input
from parser import parser
from generator import CodeGenerator

def execute_generated_code(generated_code):
    local_vars = {}
    exec(generated_code, {}, local_vars)
    result = local_vars.get('result', [])
    with open('output.txt', 'w') as f:
        f.write(str(result))

code = """
parallel(x in [1, 2, 3]) {
  x = x * 2;
  return x;
}
"""
# 词法分析
tokens = lex_input(code)
print(f"Tokens: {tokens}")

# 语法分析：传递 tokens 列表给解析器
result = parser.parse(code)
print(result)

generator = CodeGenerator()
python_code = generator.generate_code(result)
with open('out.py', 'w') as f:
    f.write(str(python_code))
print(python_code)

execute_generated_code(python_code)