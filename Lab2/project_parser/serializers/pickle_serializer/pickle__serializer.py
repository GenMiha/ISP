from project_parser.object_converter import refactor_object, restore_object


class PickleSerializer:
    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'w') as outfile:
            outfile.write(PickleSerializer.obj_to_pickle(obj))

    def dumps(self, obj):
        return PickleSerializer.obj_to_pickle(obj)

    def load(self, fp): # pragma: no cover
        with open(fp, "r") as infile:
            content = infile.read()
        return PickleSerializer.pickle_to_obj(content)

    def loads(self, s):
        return PickleSerializer.pickle_to_obj(s)

    @staticmethod
    def obj_to_pickle(obj):
        ref_obj = refactor_object(obj)
        if type(ref_obj) is int:
            return PickleSerializer.int_to_pickle(ref_obj)
        elif type(ref_obj) is float:
            return PickleSerializer.float_to_pickle(ref_obj)
        elif type(ref_obj) is bool:
            return PickleSerializer.bool_to_pickle(ref_obj)
        elif type(ref_obj) is str:
            return PickleSerializer.str_to_pickle(ref_obj)
        elif type(ref_obj) is type(None):
            return PickleSerializer.none_to_pickle(ref_obj)
        elif type(ref_obj) is list:
            return PickleSerializer.list_to_pickle(ref_obj)
        elif type(ref_obj) is dict:
            return PickleSerializer.dict_to_pickle(ref_obj)
        else:
            raise ValueError(f"{type(ref_obj)} isn't supported")

    @staticmethod
    def pickle_to_obj(pickle_str):
        null = None
        true = True
        false = False
        obj = eval(pickle_str)
        return restore_object(obj)

    @staticmethod
    def int_to_pickle(obj):
        return str(obj)

    @staticmethod
    def float_to_pickle(obj):
        return str(obj)

    @staticmethod
    def bool_to_pickle(obj):
        return str(obj).lower()

    @staticmethod
    def str_to_pickle(obj):
        obj = obj.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{obj}"'

    @staticmethod
    def none_to_pickle(obj):
        return 'null'

    @staticmethod
    def list_to_pickle(obj):
        result_str = ''
        for item in obj:
            refactored_item = ''
            if type(item) is int:
                refactored_item += PickleSerializer.int_to_pickle(item)
            elif type(item) is float:
                refactored_item += PickleSerializer.float_to_pickle(item)
            elif type(item) is bool:
                refactored_item += PickleSerializer.bool_to_pickle(item)
            elif type(item) is str:
                refactored_item += PickleSerializer.str_to_pickle(item)
            elif type(item) is type(None):
                refactored_item += PickleSerializer.none_to_pickle(item)
            elif type(item) in (list, tuple):
                refactored_item += PickleSerializer.list_to_pickle(item)
            elif type(item) is dict:
                refactored_item += PickleSerializer.dict_to_json(item)
            else:
                raise ValueError(f"{type(item)} isn't supported")
            result_str += refactored_item + ", "
        return '[' + result_str[:-2] + ']'

    @staticmethod
    def dict_to_pickle(obj):
        result_str = ''
        for key, value in obj.items():
            refactored_item = f'{PickleSerializer.str_to_pickle(str(key))}: '
            if type(value) is int:
                refactored_item += PickleSerializer.int_to_pickle(obj[key])
            elif type(value) is float:
                refactored_item += PickleSerializer.float_to_pickle(obj[key])
            elif type(value) is bool:
                refactored_item += PickleSerializer.bool_to_pickle(obj[key])
            elif type(value) is str:
                refactored_item += PickleSerializer.str_to_pickle(obj[key])
            elif type(value) is type(None):
                refactored_item += PickleSerializer.none_to_pickle(obj[key])
            elif type(value) in (list, tuple):
                refactored_item += PickleSerializer.list_to_pickle(obj[key])
            elif type(value) is dict:
                refactored_item += PickleSerializer.dict_to_pickle(obj[key])
            else:
                raise ValueError(f"{type(value)} isn't supported")
            result_str += refactored_item + ", "
        return '{' + result_str[:-2] + '}'