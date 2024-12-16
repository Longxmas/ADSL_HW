STR_TABLE = {
    'indent': "    ",
    'newline': "\n",
    'include_tpe': "from concurrent.futures import ThreadPoolExecutor"
}

class CodeGenerator:
    def __init__(self):
        self.code = ""

    def generate_parallel(self, ast):
        variable = ast['variable']
        values = ast['list']
        body = ast['body']
        
        self.code += STR_TABLE['include_tpe'] + STR_TABLE['newline']
        
        # 生成计算逻辑的函数
        self.code += self.generate_compute_function(body)
        
        # 使用生成的函数来并行计算
        self.code += f"result = list(ThreadPoolExecutor().map(compute, {values}))\n"

    def generate_compute_function(self, body):
        compute_code = '''def compute(x):\n'''
        
        for stmt in body:
            if stmt['type'] == 'assign':
                compute_code += STR_TABLE['indent']
                compute_code += f"{stmt['variable']} = {stmt['expr']['left']} * {stmt['expr']['right']}\n"
            elif stmt['type'] == 'return':
                compute_code += STR_TABLE['indent']
                compute_code += f"return {stmt['value']}"
        
        return compute_code

    def generate_code(self, ast):
        if ast['type'] == 'parallel':
            self.generate_parallel(ast)
        return self.code