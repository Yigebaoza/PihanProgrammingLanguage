import sys
from sys import exit

from parse import PihanParser

sep_length = 20


class PihanRuntime:
    def __init__(self):
        self.parser = PihanParser()

    def execute_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.readlines()
        ast = self.parser.parse(code)
        self._execute_ast(ast)

    def _execute_ast(self, ast):
        for node in ast:
            if node['type'] == 'var_decl':
                self._handle_var_decl(node)
            if node['type'] == 'callfunc':
                self._handle_callfunc(node)

    def _handle_callfunc(self, node):
        self.parser.globals[node['name']](*(node['args']))

    def _handle_var_decl(self, node):
        self.parser.globals[node['name']] = node['value_expr']

    def ipe_run(self):
        while True:
            code = input(">?")
            ast = self.parser.parse([code])
            try:
                self._execute_ast(ast)
            except Exception as e:
                print(e)
            print()


def main(argc, argv):
    runtime = PihanRuntime()
    if argc == 1:
        runtime.ipe_run()
    elif not argv[1].endswith('.ph') or argc != 2:
        print(f"Usage: {argv[0]} {argv[1].split('.')[0]}.ph")
        exit(1)

    print(f"{"-" * sep_length}Start{"-" * sep_length}")
    try:
        runtime.execute_file(argv[1])
    finally:
        print(f"{"-" * (sep_length + 1)}End{"-" * (sep_length + 1)}")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
