import ast
from pathlib import Path
from functools import wraps
from collections import defaultdict


class Object:
    def __init__(self, name, starting_line=None, ending_line=None) -> None:
        self.name = name
        self.starting_line = starting_line
        self.ending_line = ending_line
        self.members = {}

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]


class Module(Object):
    pass


class Class(Object):
    pass


class Function(Object):
    pass


class Data(Object):
    pass


class Visitor(ast.NodeVisitor):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath
        contents = Path(self.filepath).read_text()
        self.code = ast.parse(contents)
        self.lines = contents.splitlines(keepends=False)
        self.name = filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]
        self.module = None
        self.stack = []
        self.path_stack = [self.name]
        self.scope = defaultdict(dict)

    def start_visiting(self):
        self.visit(self.code)
        return self

    @property
    def parent(self):
        """
        Return the parent node while in a given visiting method.
        
        Since we append the current node to the stack
        before starting visiting a node, the last node
        is the current node, and the parent is the last-1 node.

        Returns:
            The parent node.
        """
        try:
            return self.stack[-2]
        except IndexError:
            return None

    @property
    def in_class(self):
        for parent in reversed(self.stack[:-2]):
            if isinstance(parent, ast.ClassDef):
                return True
        return False

    @property
    def parent_is_class(self):
        return isinstance(self.parent, ast.ClassDef)

    @property
    def in_init_method(self):
        for parent in reversed(self.stack[:-2]):
            if isinstance(parent, ast.FunctionDef):
                return parent.name == "__init__"
        return False

    @property
    def path(self):
        return ".".join(self.path_stack)

    
    # def visit_Constant(self, node):
    #     print(node)

    
    # def visit_Num(self, node):
    #     print(node)

    
    # def visit_Str(self, node):
    #     print(node)

    
    # def visit_FormattedValue(self, node):
    #     print(node)

    
    # def visit_JoinedStr(self, node):
    #     print(node)

    
    # def visit_Bytes(self, node):
    #     print(node)

    
    # def visit_List(self, node):
    #     print(node)

    
    # def visit_Tuple(self, node):
    #     print(node)

    
    # def visit_Set(self, node):
    #     print(node)

    
    # def visit_Dict(self, node):
    #     print(node)

    
    # def visit_Ellipsis(self, node):
    #     print(node)

    
    # def visit_NameConstant(self, node):
    #     print(node)

    
    # def visit_Name(self, node):
    #     print(node)

    
    # def visit_Load(self, node):
    #     print(node)

    
    # def visit_Store(self, node):
    #     print(node)

    
    # def visit_Del(self, node):
    #     print(node)

    
    # def visit_Starred(self, node):
    #     print(node)

    
    # def visit_Expr(self, node):
    #     print(node)

    
    # def visit_NamedExpr(self, node):
    #     print(node)

    
    # def visit_UnaryOp(self, node):
    #     print(node)

    
    # def visit_UAdd(self, node):
    #     print(node)

    
    # def visit_USub(self, node):
    #     print(node)

    
    # def visit_Not(self, node):
    #     print(node)

    
    # def visit_Invert(self, node):
    #     print(node)

    
    # def visit_BinOp(self, node):
    #     print(node)

    
    # def visit_Add(self, node):
    #     print(node)

    
    # def visit_Sub(self, node):
    #     print(node)

    
    # def visit_Mult(self, node):
    #     print(node)

    
    # def visit_Div(self, node):
    #     print(node)

    
    # def visit_FloorDiv(self, node):
    #     print(node)

    
    # def visit_Mod(self, node):
    #     print(node)

    
    # def visit_Pow(self, node):
    #     print(node)

    
    # def visit_LShift(self, node):
    #     print(node)

    
    # def visit_RShift(self, node):
    #     print(node)

    
    # def visit_BitOr(self, node):
    #     print(node)

    
    # def visit_BitXor(self, node):
    #     print(node)

    
    # def visit_BitAnd(self, node):
    #     print(node)

    
    # def visit_MatMult(self, node):
    #     print(node)

    
    # def visit_BoolOp(self, node):
    #     print(node)

    
    # def visit_And(self, node):
    #     print(node)

    
    # def visit_Or(self, node):
    #     print(node)

    
    # def visit_Compare(self, node):
    #     print(node)

    
    # def visit_Eq(self, node):
    #     print(node)

    
    # def visit_NotEq(self, node):
    #     print(node)

    
    # def visit_Lt(self, node):
    #     print(node)

    
    # def visit_LtE(self, node):
    #     print(node)

    
    # def visit_Gt(self, node):
    #     print(node)

    
    # def visit_GtE(self, node):
    #     print(node)

    
    # def visit_Is(self, node):
    #     print(node)

    
    # def visit_IsNot(self, node):
    #     print(node)

    
    # def visit_In(self, node):
    #     print(node)

    
    # def visit_NotIn(self, node):
    #     print(node)

    
    # def visit_Call(self, node):
    #     print(node)

    
    # def visit_keyword(self, node):
    #     print(node)

    
    # def visit_IfExp(self, node):
    #     print(node)

    
    # def visit_Attribute(self, node):
    #     print(node)

    
    # def visit_Subscript(self, node):
    #     print(node)

    
    # def visit_Index(self, node):
    #     print(node)

    
    # def visit_Slice(self, node):
    #     print(node)

    
    # def visit_ExtSlice(self, node):
    #     print(node)

    
    # def visit_ListComp(self, node):
    #     print(node)

    
    # def visit_SetComp(self, node):
    #     print(node)

    
    # def visit_GeneratorExp(self, node):
    #     print(node)

    
    # def visit_DictComp(self, node):
    #     print(node)

    
    # def visit_comprehension(self, node):
    #     print(node)

    
    def visit_Assign(self, node):
        print(node)

    
    def visit_AnnAssign(self, node):
        print(node)

    
    def visit_AugAssign(self, node):
        print(node)

    
    # def visit_Print(self, node):
    #     print(node)

    
    # def visit_Raise(self, node):
    #     print(node)

    
    # def visit_Assert(self, node):
    #     print(node)

    
    # def visit_Delete(self, node):
    #     print(node)

    
    # def visit_Pass(self, node):
    #     print(node)

    
    def visit_Import(self, node):
        for alias in node.names:
            self.scope[self.path][alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    
    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.scope[self.path][alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.generic_visit(node)

    
    # def visit_alias(self, node):
    #     print(node)

    
    # def visit_If(self, node):
    #     print(node)

    
    # def visit_For(self, node):
    #     print(node)

    
    # def visit_While(self, node):
    #     print(node)

    
    # def visit_Break(self, node):
    #     print(node)

    
    # def visit_Continue(self, node):
    #     print(node)

    
    # def visit_Try(self, node):
    #     print(node)

    
    # def visit_TryFinally(self, node):
    #     print(node)

    
    # def visit_TryExcept(self, node):
    #     print(node)

    
    # def visit_ExceptHandler(self, node):
    #     print(node)

    
    # def visit_With(self, node):
    #     print(node)

    
    # def visit_withitem(self, node):
    #     print(node)

    
    def visit_FunctionDef(self, node):
        if node.decorator_list:
            lineno = node.decorator_list[0].lineno
        else:
            lineno = node.lineno
        current_node = Function(node.name, starting_line=lineno, ending_line=node.end_lineno)
        self.stack[-1][node.name] = current_node

    
    # def visit_Lambda(self, node):
    #     print(node)

    
    # def visit_arguments(self, node):
    #     print(node)

    
    # def visit_arg(self, node):
    #     print(node)

    
    # def visit_Return(self, node):
    #     print(node)

    
    # def visit_Yield(self, node):
    #     print(node)

    
    # def visit_YieldFrom(self, node):
    #     print(node)

    
    # def visit_Global(self, node):
    #     print(node)

    
    # def visit_NonLocal(self, node):
    #     print(node)

    
    def visit_ClassDef(self, node):
        current_node = Class(node.name, starting_line=node.lineno, ending_line=node.end_lineno)
        self.stack[-1][node.name] = current_node
        self.stack.append(current_node)
        self.generic_visit(node)
        self.stack.pop()


    
    # def visit_AsyncFunctionDef(self, node):
    #     print(node)

    
    # def visit_Await(self, node):
    #     print(node)

    
    # def visit_AsyncFor(self, node):
    #     print(node)

    
    # def visit_AsyncWith(self, node):
    #     print(node)

    def visit_Module(self, node):
        self.module = Module(self.name, starting_line=1, ending_line=len(self.lines) + 1)
        self.stack.append(self.module)
        self.generic_visit(node)
        self.stack.pop()

    
    # def visit_Interactive(self, node):
    #     print(node)

    
    # def visit_Expression(self, node):
    #     print(node)


def parse(filepath):
    tree = ast.parse(Path(filepath).read_text())
    return Visitor(filepath).visit(tree)


if __name__ == "__main__":
    visitor = Visitor(__file__).start_visiting()
    print(visitor.root)
