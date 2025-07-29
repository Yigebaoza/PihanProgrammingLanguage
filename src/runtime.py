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
                case 'func_def':
                    self._handle_func_def(node)

    def _handle_callfunc(self, node):
        self.parser.globals[node['name']](*(node['args']))

    def _handle_var_decl(self, node):
        self.parser.globals[node['name']] = node['value_expr']

    def _handle_cs(self, node):
        if eval(node['condition'], self.parser.globals):
            ast = []
            for line in node['codes']:
                if line == '}':
                    break
                ast.append(*self.parser.parse([line]))

            self._execute_ast(ast)

    def _handle_func_def(self, node):
        """
        def {name}(args[i]...):
        \tcodes[i]\n...
        """
        def_code = f"def {node['name']}("
        for arg in node['args']:
            def_code += f"{arg}, "
        def_code = def_code+ "):\n"
        for code in node['codes']:
            def_code += f"\t{code.replace("<", "return")}\n"
        exec(def_code, self.parser.globals)

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
