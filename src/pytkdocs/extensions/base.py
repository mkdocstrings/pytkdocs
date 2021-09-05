import ast


class Extension(ast.NodeVisitor):
    def __init__(self, visitor) -> None:
        super().__init__()
        self.visitor = visitor


class Extensions:
    def __init__(self) -> None:
        self._pre_visitors_classes = []
        self._post_visitors_classes = []
        self._pre_visitors = []
        self._post_visitors = []

    @property
    def pre_visitors(self):
        return self._pre_visitors

    @property
    def post_visitors(self):
        return self._post_visitors

    def instantiate(self, parent_visitor):
        self._pre_visitors = [pre_visitor(parent_visitor) for pre_visitor in self._pre_visitors_classes]
        self._post_visitors = [post_visitor(parent_visitor) for post_visitor in self._post_visitors_classes]
        return self

    def add_pre_visitor(self, visitor):
        self._pre_visitors_classes.append(visitor)

    def add_post_visitor(self, visitor):
        self._post_visitors_classes.append(visitor)


# TODO: maybe add a method to the main visitor
# that runs the pre visitors, then some code,
# then self.generic_visit(node),
# then the post visitors, the goal being
# able to run pre- and post- methods
# after appending to the stack and before popping
# the last stack item, respectively.
def extend(method):
    def wrapped(self, node):
        for pre_visitor in self.extensions.pre_visitors:
            pre_visitor.visit(node)
        method(self, node)
        for post_visitor in self.extensions.post_visitors:
            post_visitor.visit(node)

    return wrapped
