import ast
from collections import defaultdict

from pytkdocs.dataclasses import Class, Function
from pytkdocs.extensions.base import extend


class Node:
    def __init__(self, node, parent=None) -> None:
        self.node = node
        self.parent = parent
        self.children = []

    def graft(self, node):
        self.children.append(Node(node, self))

    
class ASTTree:
    def __init__(self) -> None:
        self.node = None

    def graft(self, node):
        self.node = Node(node)
        return self.node


class DataStack:
    def __init__(self, base) -> None:
        self.stack = [base]
        self.last = None

    @property
    def module_object(self):
        return self.stack[0]

    @property
    def current_object(self):
        return self.stack[-1]

    def push(self, obj):
        self.current_object[obj.name] = obj
        self.stack.append(obj)

    def pop(self):
        self.last = self.stack.pop()


class Visitor(ast.NodeVisitor):
    def __init__(self, stack_base, base_node, extensions) -> None:
        super().__init__()
        self.extensions = extensions.instantiate(self)
        self.scope = defaultdict(dict)
        self.stack = DataStack(stack_base)
        self.current = None
        self.tree = ASTTree()
        self.node = self.tree
        self.generic_visit(base_node)

    def pop(self):
        return self.stack.pop()

    def visit(self, node: ast.AST) -> None:
        self.node = self.node.graft(node)
        for pre_visitor in self.extensions.pre_visitors:
            pre_visitor.visit(node)
        super().visit(node)
        for post_visitor in self.extensions.post_visitors:
            post_visitor.visit(node)
        self.node = self.node.parent

    @property
    def module(self):
        return self.stack[0]

    @property
    def parent(self):
        return self.stack[-1]

    @extend
    def visit_Constant(self, node):
        self.generic_visit(node)

    @extend
    def visit_Num(self, node):
        self.generic_visit(node)

    @extend
    def visit_Str(self, node):
        self.generic_visit(node)

    @extend
    def visit_FormattedValue(self, node):
        self.generic_visit(node)

    @extend
    def visit_JoinedStr(self, node):
        self.generic_visit(node)

    @extend
    def visit_Bytes(self, node):
        self.generic_visit(node)

    @extend
    def visit_List(self, node):
        self.generic_visit(node)

    @extend
    def visit_Tuple(self, node):
        self.generic_visit(node)

    @extend
    def visit_Set(self, node):
        self.generic_visit(node)

    @extend
    def visit_Dict(self, node):
        self.generic_visit(node)

    @extend
    def visit_Ellipsis(self, node):
        self.generic_visit(node)

    @extend
    def visit_NameConstant(self, node):
        self.generic_visit(node)

    @extend
    def visit_Name(self, node):
        self.generic_visit(node)

    @extend
    def visit_Load(self, node):
        self.generic_visit(node)

    @extend
    def visit_Store(self, node):
        self.generic_visit(node)

    @extend
    def visit_Del(self, node):
        self.generic_visit(node)

    @extend
    def visit_Starred(self, node):
        self.generic_visit(node)

    @extend
    def visit_Expr(self, node):
        self.generic_visit(node)

    @extend
    def visit_NamedExpr(self, node):
        self.generic_visit(node)

    @extend
    def visit_UnaryOp(self, node):
        self.generic_visit(node)

    @extend
    def visit_UAdd(self, node):
        self.generic_visit(node)

    @extend
    def visit_USub(self, node):
        self.generic_visit(node)

    @extend
    def visit_Not(self, node):
        self.generic_visit(node)

    @extend
    def visit_Invert(self, node):
        self.generic_visit(node)

    @extend
    def visit_BinOp(self, node):
        self.generic_visit(node)

    @extend
    def visit_Add(self, node):
        self.generic_visit(node)

    @extend
    def visit_Sub(self, node):
        self.generic_visit(node)

    @extend
    def visit_Mult(self, node):
        self.generic_visit(node)

    @extend
    def visit_Div(self, node):
        self.generic_visit(node)

    @extend
    def visit_FloorDiv(self, node):
        self.generic_visit(node)

    @extend
    def visit_Mod(self, node):
        self.generic_visit(node)

    @extend
    def visit_Pow(self, node):
        self.generic_visit(node)

    @extend
    def visit_LShift(self, node):
        self.generic_visit(node)

    @extend
    def visit_RShift(self, node):
        self.generic_visit(node)

    @extend
    def visit_BitOr(self, node):
        self.generic_visit(node)

    @extend
    def visit_BitXor(self, node):
        self.generic_visit(node)

    @extend
    def visit_BitAnd(self, node):
        self.generic_visit(node)

    @extend
    def visit_MatMult(self, node):
        self.generic_visit(node)

    @extend
    def visit_BoolOp(self, node):
        self.generic_visit(node)

    @extend
    def visit_And(self, node):
        self.generic_visit(node)

    @extend
    def visit_Or(self, node):
        self.generic_visit(node)

    @extend
    def visit_Compare(self, node):
        self.generic_visit(node)

    @extend
    def visit_Eq(self, node):
        self.generic_visit(node)

    @extend
    def visit_NotEq(self, node):
        self.generic_visit(node)

    @extend
    def visit_Lt(self, node):
        self.generic_visit(node)

    @extend
    def visit_LtE(self, node):
        self.generic_visit(node)

    @extend
    def visit_Gt(self, node):
        self.generic_visit(node)

    @extend
    def visit_GtE(self, node):
        self.generic_visit(node)

    @extend
    def visit_Is(self, node):
        self.generic_visit(node)

    @extend
    def visit_IsNot(self, node):
        self.generic_visit(node)

    @extend
    def visit_In(self, node):
        self.generic_visit(node)

    @extend
    def visit_NotIn(self, node):
        self.generic_visit(node)

    @extend
    def visit_Call(self, node):
        self.generic_visit(node)

    @extend
    def visit_keyword(self, node):
        self.generic_visit(node)

    @extend
    def visit_IfExp(self, node):
        self.generic_visit(node)

    @extend
    def visit_Attribute(self, node):
        self.generic_visit(node)

    @extend
    def visit_Subscript(self, node):
        self.generic_visit(node)

    @extend
    def visit_Index(self, node):
        self.generic_visit(node)

    @extend
    def visit_Slice(self, node):
        self.generic_visit(node)

    @extend
    def visit_ExtSlice(self, node):
        self.generic_visit(node)

    @extend
    def visit_ListComp(self, node):
        self.generic_visit(node)

    @extend
    def visit_SetComp(self, node):
        self.generic_visit(node)

    @extend
    def visit_GeneratorExp(self, node):
        self.generic_visit(node)

    @extend
    def visit_DictComp(self, node):
        self.generic_visit(node)

    @extend
    def visit_comprehension(self, node):
        self.generic_visit(node)

    @extend
    def visit_Assign(self, node):
        self.generic_visit(node)

    @extend
    def visit_AnnAssign(self, node):
        self.generic_visit(node)

    @extend
    def visit_AugAssign(self, node):
        self.generic_visit(node)

    @extend
    def visit_Print(self, node):
        self.generic_visit(node)

    @extend
    def visit_Raise(self, node):
        self.generic_visit(node)

    @extend
    def visit_Assert(self, node):
        self.generic_visit(node)

    @extend
    def visit_Delete(self, node):
        self.generic_visit(node)

    @extend
    def visit_Pass(self, node):
        self.generic_visit(node)

    @extend
    def visit_Import(self, node):
        # for alias in node.names:
        #     self.scope[self.path][alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    @extend
    def visit_ImportFrom(self, node):
        # for alias in node.names:
        #     self.scope[self.path][alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.generic_visit(node)

    @extend
    def visit_alias(self, node):
        self.generic_visit(node)

    @extend
    def visit_If(self, node):
        self.generic_visit(node)

    @extend
    def visit_For(self, node):
        self.generic_visit(node)

    @extend
    def visit_While(self, node):
        self.generic_visit(node)

    @extend
    def visit_Break(self, node):
        self.generic_visit(node)

    @extend
    def visit_Continue(self, node):
        self.generic_visit(node)

    @extend
    def visit_Try(self, node):
        self.generic_visit(node)

    @extend
    def visit_TryFinally(self, node):
        self.generic_visit(node)

    @extend
    def visit_TryExcept(self, node):
        self.generic_visit(node)

    @extend
    def visit_ExceptHandler(self, node):
        self.generic_visit(node)

    @extend
    def visit_With(self, node):
        self.generic_visit(node)

    @extend
    def visit_withitem(self, node):
        self.generic_visit(node)

    @extend
    def visit_FunctionDef(self, node):
        if node.decorator_list:
            lineno = node.decorator_list[0].lineno
        else:
            lineno = node.lineno
        current_node = Function(self.module.filepath, node.name, starting_line=lineno, ending_line=node.end_lineno)
        self.parent[node.name] = current_node

    @extend
    def visit_Lambda(self, node):
        self.generic_visit(node)

    @extend
    def visit_arguments(self, node):
        self.generic_visit(node)

    @extend
    def visit_arg(self, node):
        self.generic_visit(node)

    @extend
    def visit_Return(self, node):
        self.generic_visit(node)

    @extend
    def visit_Yield(self, node):
        self.generic_visit(node)

    @extend
    def visit_YieldFrom(self, node):
        self.generic_visit(node)

    @extend
    def visit_Global(self, node):
        self.generic_visit(node)

    @extend
    def visit_NonLocal(self, node):
        self.generic_visit(node)

    @extend
    def visit_ClassDef(self, node):
        self.current = Class(self.module.filepath, node.name, starting_line=node.lineno, ending_line=node.end_lineno)
        self.parent[node.name] = self.current
        self.stack.append(self.current)
        self.generic_visit(node)
        self.stack.pop()

    @extend
    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)

    @extend
    def visit_Await(self, node):
        self.generic_visit(node)

    @extend
    def visit_AsyncFor(self, node):
        self.generic_visit(node)

    @extend
    def visit_AsyncWith(self, node):
        self.generic_visit(node)

    @extend
    def visit_Module(self, node):
        self.generic_visit(node)

    @extend
    def visit_Interactive(self, node):
        self.generic_visit(node)

    @extend
    def visit_Expression(self, node):
        self.generic_visit(node)
