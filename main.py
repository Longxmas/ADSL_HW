import os
import re
import subprocess
from lexer import lexer, lex_input
from parser import parser, format_ast
from generator import Generator
import argparse

def remove_comments(code):
    # 匹配 /*... */ 的多行注释，并删除
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # 匹配 //... 的单行注释，并删除
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    return code


def Parse(test_name):
    code = ""
    dir_path = 'testcase/'
    if test_name == "full":
        file_path = "1_full.c"
    elif test_name == "parallel":
        file_path = "2_parallel.c"
    elif test_name == "merge_sort":
        file_path = "3_merge_sort.c"
    elif test_name == "gemv":
        file_path = "4_gemv.c"
    elif test_name == "nest":
        file_path = "5_nest.c"
    else:
        print(f"不支持的测试名称: {test_name}，请选择full、parallel、merge_sort、gemv或nest。")
        return None

    try:
        with open(dir_path + file_path, 'r', encoding='utf-8') as f:
            lines = []
            for line in f:
                lines.append(line)
            code = "".join(lines)
    except FileNotFoundError:
        print(f"{file_path} 文件不存在，请确保该文件已存在。")
        return None

    return code


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("test_name", type=str, help="测试名称，可选值为full、parallel、merge_sort或gemv。")
    args = argparser.parse_args()

    is_gemv_mode = args.test_name == "gemv"

    code = Parse(args.test_name)
    code = remove_comments(code)

    # 词法分析
    try:
        tokens = lex_input(code)
        print("词法分析成功")
    except Exception as e:
        print(f"词法分析出现错误: {str(e)}")
        return

    # 语法分析
    try:
        result = parser.parse(code)
        result.build()
        print("语法分析成功")
    except Exception as e:
        print(f"语法分析出现错误: {str(e)}")
        return

    # 代码生成
    try:
        generator = Generator(result)
        generator.generate()
        with open("code_output.go", "w", encoding='utf-8') as f:
            f.write(generator.code)
        print("代码生成成功")
    except Exception as e:
        print(f"代码生成出现错误: {str(e)}")
        return

    if is_gemv_mode:
        # 在gemv测试模式下，使用subprocess模块运行python get_input.py命令，并等待其执行完成
        try:
            process = subprocess.Popen(["python", "get_input.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode!= 0:
                print(f"运行python get_input.py出现错误，错误信息如下：\n{stderr.decode('utf-8')}")
                return
        except FileNotFoundError:
            print("python get_input.py文件不存在，请确保该文件已存在")
            return

        # 尝试从gemv.txt中读取第一行作为后续go命令的输入
        try:
            with open('gemv.txt', 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                second_line = f.readline().strip()
        except FileNotFoundError:
            print("gemv.txt文件不存在，请确保该文件已生成")
            return
        
        # 从gemv.txt读取的第一行作为输入传入go run code_output.go命令
        # os.system(f'go run code_output.go {first_line}')
        process = subprocess.Popen(
            ['go', 'run', 'code_output.go'],  # Go 命令和文件
            stdin=subprocess.PIPE,  # 启用标准输入管道
            stdout=subprocess.PIPE,  # 获取标准输出
            stderr=subprocess.PIPE,  # 获取标准错误输出
        )

        # 将 first_line 变量传递给 Go 程序
        stdout, stderr = process.communicate(input=first_line.encode())  # 传递的输入需要编码成字节

        # 打印 Go 程序的输出
        print(stdout.decode())  # 获取并打印 Go 程序的输出
        # 然后输出第二行表示正确结果
        print("GEMV正确结果为: " + second_line)
    else:
        print("运行程序 >>> go run code_output.go")
        os.system(f'go run code_output.go')


if __name__ == "__main__":
    main()