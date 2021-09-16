import builtins
import types
import logging
import inspect


logging.basicConfig(
    level=logging.WARNING, filename="warning.log", format="%(levelname)s: %(message)s"
)

list_of_dumped = []

func_attributes = (
    "__name__",
    "__qualname__",
    "__doc__",
    "__dict__",
    "__module__",
    "__closure__",
    "__defaults__",
    "__kwdefaults__",
    "__annotations__",
    "__code__",
)

code_attributes = (
    "co_argcount",
    "co_posonlyargcount",
    "co_kwonlyargcount",
    "co_nlocals",
    "co_stacksize",
    "co_flags",
    "co_code",
    "co_consts",
    "co_names",
    "co_varnames",
    "co_filename",
    "co_name",
    "co_firstlineno",
    "co_lnotab",
    "co_freevars",
    "co_cellvars",
)

module_attributes = ("__name__", "__doc__")

default_types = (
    *(
        getattr(builtins, key)
        for key in dir(builtins)
        if inspect.isclass(getattr(builtins, key))
    ),
    *(
        getattr(types, key)
        for key in dir(types)
        if inspect.isclass(getattr(types, key))
    ),
)


def dump_as_is(obj):
    return obj


def dump_tuple(tuple_obj):
    tmp_list = []
    for obj in tuple_obj:
        try:
            tmp_list.append(dump_obj(obj))
        except TypeError as error:
            logging.warning(
                "<{}> was skipped because of {}".format(dump_hint(obj), error)
            )
    return tmp_list


def dump_id(obj):
    return hex(id(obj))


def dump_hint(obj):
    return "'{}' of '{}' at {}".format(
        obj.__name__ if hasattr(obj, "__name__") else "instance",
        type(obj).__name__,
        dump_id(obj),
    )


def dump_simple_object(obj):
    list_of_dumped.append(id(obj))
    return {
        "__id__": dump_id(obj),
        "__class__": dump_obj(type(obj)),
    }


def dump_value(obj, value):
    dict_to_dump = dump_simple_object(obj)
    dict_to_dump["__value__"] = dump_obj(value)
    return dict_to_dump


def dump_special_attributes(obj, specal_attributes):
    dict_to_dump = dump_simple_object(obj)
    for attr in specal_attributes:
        dict_to_dump[attr] = dump_obj(getattr(obj, attr))
    return dict_to_dump


def dump_func(func):
    def dump_globals(code):
        glob.extend(code.co_names)
        for const in code.co_consts:
            if type(const) is types.CodeType:
                dump_globals(const)

    glob = []
    dump_globals(func.__code__)
    glob_dct = {var: func.__globals__[var] for var in func.__globals__ if var in glob}
    return {
        **dump_special_attributes(func, func_attributes),
        "__globals__": dump_obj(glob_dct),
    }


implemented = {
    type(None): dump_as_is,
    bool: dump_as_is,
    object: dump_simple_object,
    int: dump_as_is,
    float: dump_as_is,
    complex: lambda obj: dump_value(obj, (obj.real, obj.imag)),
    str: dump_as_is,
    list: lambda obj: dump_value(obj, tuple(obj)),
    tuple: dump_tuple,
    range: lambda obj: dump_value(obj, (obj.start, obj.stop, obj.step)),
    bytes: lambda obj: dump_value(obj, obj.hex(" ", 1)),
    bytearray: lambda obj: dump_value(obj, obj.hex(" ", 1)),
    set: lambda obj: dump_value(obj, tuple(obj)),
    frozenset: lambda obj: dump_value(obj, tuple(obj)),
    dict: lambda obj: dump_value(obj, tuple(obj.items())),
    types.FunctionType: lambda obj: dump_func(obj),
    types.CodeType: lambda obj: dump_special_attributes(obj, code_attributes),
    types.CellType: lambda obj: dump_value(obj, obj.cell_contents),
    types.ModuleType: lambda obj: dump_special_attributes(obj, module_attributes),
}

unimplemented = tuple(cls for cls in default_types if cls not in implemented)


def dump_obj(obj):
    if obj in default_types:
        return {"__id__": str(obj)}
    if id(obj) in list_of_dumped:
        return {"__id__": dump_hint(obj)}
    if type(obj) in unimplemented: # неподдерживаемый для нас тип
        raise TypeError("<{}> has unimplemented type".format(dump_hint(obj)))
    return implemented[type(obj)](obj)


def dump(obj):
    list_of_dumped.clear()
    return dump_obj(obj)
