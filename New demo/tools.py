import functools as _functools
import itertools as _itertools
import typing as _typing
import heapq as heapq
import collections as _collections
import inspect as _inspect

from loguru import logger as _logger


_LISTENING_METHOD_ATTR_NAME = "_listening_codes"  # listening装饰器修改的函数属性

_WARNING_DO_NOT_DECORATE_PRIVATE = """Do not use the `listening` decorator on private methods!
Private methods can be inherited by subclasses and captured by `find_listening_methods`.  
Additionally, Python's name mangling makes it very difficult to override private methods from the parent class.  

请不要对私有方法使用 `listening` 装饰器！  
私有方法不仅会被子类继承，还会被 `find_listening_methods` 捕捉到。  
此外, Python的名称修饰机制使得重写父类的私有方法变得非常困难。"""
# 说得好！

def listening(code: int) -> _typing.Callable[[_typing.Callable], _typing.Callable]:
    """
    listening装饰器
    用于标记监听事件的方法

    Parameters
    ---
    code : int
        事件代码
        监听这个代码，被修饰函数将会响应这个代码对应的事件
        例如 @listening(114514)
            def AyachiNene(Yuzusoft=0721):
                return 1919810
        # TODO:

    Returns
    ---
    _typing.Callable[[_typing.Callable], _typing.Callable]
        装饰器
    """

    def decorator(
            func: _typing.Callable[["_colls.EventLike"], None]
    ) -> _typing.Callable[["_colls.EventLike"], None]:
        if func.__name__.startswith("__"):
            _logger.warning(_WARNING_DO_NOT_DECORATE_PRIVATE)
            func.__qualname__
        if not hasattr(func, _LISTENING_METHOD_ATTR_NAME):
            setattr(func, _LISTENING_METHOD_ATTR_NAME, set())
        getattr(func, _LISTENING_METHOD_ATTR_NAME).add(code)
        return func

    return decorator


