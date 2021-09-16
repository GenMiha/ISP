import builtins
import inspect
import types
from importlib import import_module

loaded = {}
func_glob = {}

moduleattrs = ("__name__", "__doc__")

funcattrs_construct = (
    "__code__",
    "__globals__",
    "__name__",
    "__defaults__",
    "__closure__",
)

funcattrs_rest = (
    "__qualname__",
    "__doc__",
    "__dict__",
    "__module__",
    "__kwdefaults__",
    "__annotations__",
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

default_types = {
    **{
        str(getattr(builtins, key)): getattr(builtins, key)
        for key in dir(builtins)
        if inspect.isclass(getattr(builtins, key))
    },
    **{
        str(getattr(types, key)): getattr(types, key)
        for key in dir(types)
        if inspect.isclass(getattr(types, key))
    },
}


def load_id(id_str):
    return int(id_str.rpartition(" at ")[2], 0)


def load_id_data(id_str):
    if id_str.startswith("<"):
        return (default_types[id_str], True)
    else:
        id_int = load_id(id_str)
        return loaded.get(id_int, (id_int, False))


def load_dict(dct):
    return {load_obj(pair[0]): load_obj(pair[1]) for pair in dct["__value__"]}


def load_func(dct):
    try:
        print(dct['__code__'])
    except Exception:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print(dct)
    tmp_dct = {
        key: (load_obj(dct[key]) if not key == "__globals__" else func_glob)
        for key in funcattrs_construct
    }

    func = types.FunctionType(*tmp_dct.values())
    loaded[load_id(dct["__id__"])] = (func, True)
    func_glob.update(load_obj(dct["__globals__"]))

    for key in funcattrs_rest:
        setattr(func, key, load_obj(dct[key]))

    return func


implemented = {
    object: lambda dct: object(),
    complex: lambda dct: complex(*dct["__value__"]),
    list: lambda dct: list(dct["__value__"]),
    range: lambda dct: range(*dct["__value__"]),
    bytes: lambda dct: bytes.fromhex(dct["__value__"]),
    bytearray: lambda dct: bytearray.fromhex(dct["__value__"]),
    set: lambda dct: set(dct["__value__"]),
    frozenset: lambda dct: frozenset(dct["__value__"]),
    dict: load_dict,
    types.FunctionType: load_func,
    types.CodeType: lambda dct: types.CodeType(
        *(load_obj(dct[key]) for key in code_attributes)
    ),
    types.CellType: lambda dct: types.CellType(load_obj(dct["__value__"])),
    types.ModuleType: lambda dct: import_module(dct["__name__"]),
}


def load_obj(obj_to_load):
    if type(obj_to_load) is list:
        return tuple(load_obj(element) for element in obj_to_load)

    if not type(obj_to_load) is dict:
        return obj_to_load
    
    tmp_obj, is_loaded = load_id_data(obj_to_load["__id__"])
    if is_loaded:
        return tmp_obj

    cls = load_obj(obj_to_load["__class__"])

    obj = implemented[cls](obj_to_load)

    loaded[tmp_obj] = (obj, True)

    return obj


def load(obj_to_load, globs={}):
    func_glob.clear()
    func_glob.update(globs)
    loaded.clear()
    return load_obj(obj_to_load)
