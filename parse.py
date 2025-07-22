import re

from builtin import *


class PihanParser:
    def __init__(self):
        self.builtins = PHAN_BUILTINS  # 从builtin模块导入的预定义函数
        self.locals = {}
        self.globals = {**self.builtins}

    def parse(self, code_lines):
        """解析PFH代码并生成可执行结构"""
        ast = []
        for line in code_lines:
            line = line.strip()
            if not line or line.startswith("/'"):  # 跳过空行和注释
                continue

            if line.startswith('var '):
                ast.append(self._parse_var_declaration(line))
            # 添加其他语法解析...
            elif re.search(r"[()]", line): # 匹配函数调用
                ast.append(self._parse_callfunc(line))
            # 添加其他语法解析...
        return ast

    def _parse_callfunc(self, line):
        # 解析 func_name(content, so) 格式
        name = line.split('(', 1)[0].strip()
        parts = line.split('(', 1)[1].rsplit(')', 1)[0].split(',')
        
        return {
            'type': 'callfunc',
            'name': name,
            'content': parts[0].strip(),
            'stream': parts[1].strip()
        }

    def _parse_var_declaration(self, line):
        # 解析 var type name = value 格式
        parts = line.strip("var ").split('=', 1)
        # name = func(args)
        # "name", "ward("InputYourname:", io)"
        var_def = parts[0].strip().split()
        value = parts[1]
        if re.search("[()]", value):  # 如果value是函数调用，则解析它
            func = self._parse_callfunc(value)
            name = func['name']
            content = func['content']
            st = func['stream']
            value = self.globals[name](content, st)
        elif re.search(r"[+\-*/]", value):  # 如果value是表达式，则计算它
            value = str(eval(value, self.globals, self.locals))
        else:
            value.strip()
        return {
            'type': 'var_decl',
            'name': var_def[0],
            'value_expr': value
        }
