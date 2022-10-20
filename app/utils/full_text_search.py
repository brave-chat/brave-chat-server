from sqlalchemy.ext.compiler import (
    compiles,
)
from sqlalchemy.schema import (
    Constraint,
)


class Fulltext(Constraint):
    def __init__(self, arg):
        self.arg = arg
        super().__init__()


@compiles(Fulltext)
def compile_ft(elem, compiler, **kw):
    return f"FULLTEXT({elem.arg})"
