"""A collection of utilities used across the project."""

def concreter(abclass):
    """
    >>> import abc
    >>> import six
    >>> @six.add_metaclass(abc.ABCMeta)
    ... class Abstract(metaclass=abc.ABCMeta):
    ...     @abc.abstractmethod
    ...     def bar(self):
    ...        pass

    >>> c = concreter(Abstract)
    >>> c.__name__
    'dummy_concrete_Abstract'
    >>> c().bar() # doctest: +ELLIPSIS
    (<abc_utils.Abstract object at 0x...>, (), {})
    """

    if not "__abstractmethods__" in abclass.__dict__:
        return abclass

    new_dict = abclass.__dict__.copy()
    for abstractmethod in abclass.__abstractmethods__:
        #replace each abc method or property with an identity function:
        new_dict[abstractmethod] = lambda x, *args, **kw: (x, args, kw)
    #creates a new class, with the overriden ABCs:
    return type("dummy_concrete_%s" % abclass.__name__, (abclass,), new_dict)
