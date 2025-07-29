import re

from builtin import *


class PihanParser:
    def __init__(self):
        self.builtins = PIHAN_BUILTINS  # 从builtin模块导入的预定义函数
        self.locals = {}
        self.globals = {**self.builtins}
        self.cs_stack = []  # 条件语句栈
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
            elif line.startswith("'"):
                continue

            in_cs = True if line.startswith("in::") else False  # 是否在条件语句中
            in_def_func = True if line.startswith("func") else False  # 是否正在定义函数
            if line.startswith('var') and not in_cs:  # 匹配变量声明
                var = self._parse_var_declaration(line)
                ast.append(var)
                self.globals[var['name']] = var['value_expr']
            elif re.search(r"[()]", line) and not in_cs and not in_def_func:  # 匹配函数调用
                call = self._parse_call(line)
                ast.append(call)
            elif line.startswith("jud "):  # 匹配条件语句
                cs = self._parse_jud_cs(line, code_lines)
                self.cs_stack.append(cs)
                ast.append(cs)
            elif line.startswith("not "):  # 匹配非条件语句
                cs = self._parse_not_cs(line, code_lines)
                ast.append(cs)
            elif line.startswith("func "):  # 匹配函数定义
                func = self._parse_func_def(line, code_lines)
                ast.append(func)
                self.globals[func['name']] = func
        return ast

    def _parse_call(self, line):
        # 解析 func_name(content, so) 格式
        func = line.split('(', 1)
        name = func[0].strip()  # 获取函数名
        strip = func[1].rstrip(")").strip()
        if strip == "":
            args = []
        else:
            args = eval(strip, self.globals)
            if not (isinstance(args, tuple) or isinstance(args, list)):
                args = [args]

        return {
            'type': 'callfunc',
            'name': name,
            'args': args,
        }

    def _parse_var_declaration(self, line):
        # 解析 var name = res 格式
        parts = line.replace("var ", "").split('=', 1)
        name = parts[0].strip()
        res = parts[1].strip()
        if re.search("[()]", res):  # 如果value是函数调用，则解析它
            func = self._parse_call(res)
            func_name = func['name']
            args = func['args']
            call = self.globals[func_name]
            try:
                res = call(*args)
            except TypeError:
                for code in call['codes']:
                    if code.startswith("<"):
                        try:
                            code = code.replace("<", "").strip()
                            res = eval(code, *self.all)
                        except NameError:
                            real_args = {k.replace(" ", ""):v for k, v in zip(call['args'], args)}
                            res = eval(code, {**self.globals, **self.locals, **real_args})

                        break
                    exec(code, *self.all)
        elif re.search(r"[+\-*/]", res):  # 如果value是表达式，则计算它
            res = str(eval(res, *self.all))

        return {
            'type': 'var_decl',
            'name': name,
            'value_expr': res
        }

    def _parse_jud_cs(self, line, codes):
        """
        jud cond?{code...}
        """
        parts = line.split("jud ")[1]
        split = parts.split("?")
        condition = split[0]  # 条件表达式
        # the line of index ~ end of index
        start = codes.index(line + "\n") + 1
        stop = 0
        for code_col in range(start, len(codes)):
            if not code_col:
                continue
            elif codes[code_col].strip() == "}":
                stop = code_col + 1
                break
        body = [codes[code_col].replace("in::", "").strip()
                for code_col in range(start, stop)
                if code_col]
        del body[-1]
        return {
            'type': 'cs',
            'condition': condition,
            'codes': body
        }

    def _parse_not_cs(self, line, codes):
        """
        not {code...}
        :param codes:
        """
        body = []
        for code_col in range(codes.index(line+"\n")+1, len(codes)):
            if not code_col:
                continue
            elif codes[code_col].strip() == "}":
                break
            body.append(codes[code_col].replace("in::", "").strip())
        condition = self.cs_stack[-1]['condition']  # 条件表达式
        return {
            'type': 'cs',
            'condition': f"not ({condition})",
            'codes': body
        }

    def _parse_func_def(self, line, codes):
        """
        func_name(disp nop)&{
            code...
        }
        """
        parts = line.strip("func ").split("&")
        head = parts[0].strip()
        name = head.split('(')[0].strip()  # 函数名
        args = head.split('(')[1].rstrip(')').strip().split(',')
        start = codes.index(line+"\n")+1
        stop = 0
        for code_col in range(start, len(codes)):
            if not code_col:
                continue
            elif codes[code_col].strip() == "}":
                stop = code_col + 1
                break
        args = [args] if not isinstance(args, list) else args
        args = [] if args[0] == ["nop"] else args
        body = [codes[code_col].replace("in::", "").strip()
                for code_col in range(start, stop)
                if code_col]
        del body[-1]

        return {
            "type": "func_def",
            "name": name,
            "args": args,
            "codes": body
        }
