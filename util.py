import ast
import inspect

def get_args_names():
    class FuncCallArgsVisitor(ast.NodeVisitor):
        def __init__(self, func_name):
            self.func_name = func_name
            self.call_args = []

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
                self.call_args = node.args
                return
            self.generic_visit(node)


    def get_func_args(tree, fname):
        visitor = FuncCallArgsVisitor(fname)
        visitor.visit(tree)
        return visitor.call_args


    def get_calling_ast_args(frame, fname):
        try:
            source_lines = inspect.getsourcelines(frame.f_code)[0]
        except OSError:  # In case we can't get source (e.g. in REPL)
            raise ValueError("Cannot get source code for frame")

        ast_node = ast.parse("\n".join(source_lines).strip())
        return get_func_args(ast_node, fname)


    # Get the caller's frame
    caller_frame = inspect.currentframe().f_back
    caller_caller_frame = caller_frame.f_back

    # Get the AST of the calling line
    calling_args = get_calling_ast_args(caller_caller_frame, caller_frame.f_code.co_name)

    return [ast.unparse(a) for a in calling_args]

