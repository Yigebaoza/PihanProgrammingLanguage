import re

from builtin import *


class PihanParser:
    def __init__(self):
        self.builtins = PHAN_BUILTINS  # 从builtin模块导入的预定义函数
        self.locals = {}
        self.globals = {**self.builtins}
        self.all = self.globals, self.locals  # 全局命名空间和局部命名空间

    def parse(self, code_lines):
        """解析PFH代码并生成可执行结构"""
        ast = []
        for line in code_lines:
            line = line.strip()
            if not line or line.startswith("/'") or line.startswith("'/"):  # 跳过空行和注释
                continue
            elif line.startswith("//"):  # 跳过注释行
                continue

            if line.startswith('var'):
                var = self._parse_var_declaration(line)
                ast.append(var)
                self.globals[var['name']] = var['value_expr']

            # 添加其他语法解析...
            elif re.search(r"[()]", line):  # 匹配函数调用
                call = self._parse_call(line)
                ast.append(call)
                
            # 添加其他语法解析...
        return ast

    def _parse_call(self, line):
        # 解析 func_name(content, so) 格式
        func = line.split('(', 1)
        name = func[0].strip()  # 获取函数名
        strip = func[1].strip(")").strip()
        if strip == "":
            args = []
        else:
            args = eval(strip, *self.all)

        return {
            'type': 'callfunc',
            'name': name,
            'args': args,
        }

    def _parse_var_declaration(self, line):
        # 解析 name, res 格式
        parts = line.strip("var ").split('=', 1)
        name = parts[0].strip()
        res = parts[1].strip()
        if re.search("[()]", res):  # 如果value是函数调用，则解析它
            func = self._parse_call(res)
            func_name = func['name']
            args = func['args']
            res = self.globals[func_name](*args)
        elif re.search(r"[+\-*/]", res):  # 如果value是表达式，则计算它
            res = str(eval(res, self.globals, self.locals))
            
        return {
            'type': 'var_decl',
            'name': name,
            'value_expr': res
        }
