from parse import PihanParser


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
            match node['type']:
                case 'var_decl':
                    self._handle_var_decl(node)
                case 'callfunc':
                    self._handle_callfunc(node)
                case 'cs':
                    self._handle_cs(node)

    def _handle_callfunc(self, node):
        self.parser.globals[node['name']](*(node['args']))

    def _handle_var_decl(self, node):
        self.parser.globals[node['name']] = node['value_expr']

    def _handle_cs(self, node):
        if eval(node['condition'], self.parser.globals):
            for line in node['codes']:
                if line == '}':
                    break
                exec(line.strip("var").strip(), *self.parser.all)

    def ipe_run(self):
        while True:
            code = input(">?")
            try:
                ast = self.parser.parse([f"writeln({code}, so)"])
            except:
                ast = self.parser.parse([code])
            try:
                self._execute_ast(ast)
            except Exception as e:
                print(e)
