class ScopeError(Exception):
    """The scope refused the computation (a CatalaError of its runtime)."""


class UnsupportedType(TypeError):
    """An input type that has no generic conversion from JSON."""
