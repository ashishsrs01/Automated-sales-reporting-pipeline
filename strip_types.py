import ast
import os
import glob
from pathlib import Path

class SimplifyCode(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.returns = None
        for arg in node.args.args:
            arg.annotation = None
        if node.args.posonlyargs:
            for arg in node.args.posonlyargs:
                arg.annotation = None
        if node.args.kwonlyargs:
            for arg in node.args.kwonlyargs:
                arg.annotation = None
        if node.args.vararg:
            node.args.vararg.annotation = None
        if node.args.kwarg:
            node.args.kwarg.annotation = None
        
        if ast.get_docstring(node):
            if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                node.body.pop(0)

        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.decorator_list = []
        
        if ast.get_docstring(node):
            if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                node.body.pop(0)

        fields = []
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign):
                if isinstance(stmt.target, ast.Name):
                    fields.append(stmt.target.id)
            else:
                new_body.append(stmt)
        
        if fields:
            init_args = [ast.arg(arg='self', annotation=None)] + [ast.arg(arg=f, annotation=None) for f in fields]
            init_body = [
                ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=f, ctx=ast.Store())],
                    value=ast.Name(id=f, ctx=ast.Load())
                ) for f in fields
            ]
            
            init_func = ast.FunctionDef(
                name='__init__',
                args=ast.arguments(
                    posonlyargs=[],
                    args=init_args,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                    vararg=None,
                    kwarg=None
                ),
                body=init_body,
                decorator_list=[],
                returns=None,
                type_comment=None
            )
            new_body.insert(0, init_func)
        
        node.body = new_body
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        if node.value:
            return ast.Assign(targets=[node.target], value=node.value)
        return None

    def visit_ImportFrom(self, node):
        if node.module == '__future__':
            return None
        if node.module == 'dataclasses':
            return None
        return node

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"Failed to parse {filepath}: {e}")
        return
    
    transformer = SimplifyCode()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    
    try:
        new_code = ast.unparse(new_tree)
    except Exception as e:
        print(f"Failed to unparse {filepath}: {e}")
        return
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_code)

def main():
    src_dir = Path("c:/Users/Ashish sharma/Downloads/Automated-sales-reporting-pipeline/src")
    for py_file in src_dir.rglob("*.py"):
        process_file(py_file)

if __name__ == "__main__":
    main()
