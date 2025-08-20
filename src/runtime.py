from io import BufferedWriter

from parse import PihanParser
from pvm import PihanVirtualMachine, ISA as ISA
from typing import Any

ISAR = {j: i for i, j in ISA.items()}
nts = {}

def concat_instruction_with_text(command: str, text: str) -> bytes:
    # 统一转换为bytes类型
    instruction = ISAR[command.strip()]
    text_bytes = text.encode('utf-8')  # 默认UTF-8编码

    return instruction + text_bytes

def gen_write_command(f: BufferedWriter):
    def write_command(command: str, a: str, b: str):
        f.write(concat_instruction_with_text(command, f" {a} {b}\n"))
    return write_command

class PihanRuntime:
    def __init__(self) -> None:
        self.parser = PihanParser()
        self.pvm = PihanVirtualMachine()
        self.var_count = 0

    def execute_file(self, filename: str, filetype: str) -> None:
        if filetype == "ph":
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.readlines()
            ast = self.parser.parse(code)
            self._execute_ast(ast)
        else:
            with open(f"{filename}.phc", 'rb') as f:
                self.pvm.exec_file(f)

    def _execute_ast(self, ast: list[dict[str, Any]]) -> None:
        for node in ast:
            match node['type']:
                case 'var_decl':
                    self._handle_var_decl(node)
                case 'callfunc':
                    self._handle_callfunc(node)
                case 'cs':
                    self._handle_cs(node)
                case 'func_def':
                    self._handle_func_def(node)

    def _handle_callfunc(self, node: dict[str, Any]) -> None:
        self.parser.globals[node['name']](*(node['args']))

    def _handle_var_decl(self, node: dict[str, Any]) -> None:
        self.parser.globals[node['name']] = node['value_expr']

    def _handle_cs(self, node: dict[str, Any]):
        if eval(node['condition'], self.parser.globals):
            ast = []
            for line in node['codes']:
                if line == '}':
                    break
                ast.append(*self.parser.parse([line]))

            self._execute_ast(ast)

    def _handle_func_def(self, node: dict[str, list|object]):
        """
        def {name}(args[i]...):
        \tcodes[i]\n...
        """
        def_code = f"def {node['name']}("
        for arg in node['args']:
            def_code += f"{arg}, "
        def_code = def_code+ "):\n"
        for code in node['codes']:
            def_code += f"\t{code.replace('<', 'return')}\n"
        exec(def_code, self.parser.globals)

    def ipe_run(self):
        while True:
            code = input(">?")
            try:
                ast = self.parser.parse([f"writeln({code}, so)"])
            except Exception as e:
                e.args = ()
                ast = self.parser.parse([code])
            try:
                self._execute_ast(ast)
            except Exception as e:
                print(f"Runtime Error: {e}")

    def gen_pic_file(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            with open(f"{filename.split(".")[0]}.phc", "wb") as w:
                write_command = gen_write_command(w)
                ast = self.parser.parse(f.readlines())
                for node in ast:
                    match node["type"]:
                        case 'var_decl':
                            write_command("load", node["name"], "\x00")
                            write_command("setv", node["name"], node["value_expr"])
                        case 'callfunc':
                            new_line_oper = "\x00" if node["name"].endswith("ln") else "\x01"
                            write_command("show", node["args"][0], new_line_oper)
                        case 'cs':
                            pass
                        case 'func_def':
                            pass

