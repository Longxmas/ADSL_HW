from lexer import lexer, lex_input
from parser import parser, format_ast
from generator import Generator

def execute_generated_code(generated_code):
    local_vars = {}
    exec(generated_code, {}, local_vars)
    result = local_vars.get('result', [])
    with open('output.txt', 'w') as f:
        f.write(str(result))

code = """
int main() {
  parallel (int x, int y, int z) in a, b, c {
    z << add(x, y);
    z >> add(x, y);
  }
  return 0;
}
"""
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