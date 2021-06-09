from Lab2.project_parser.serializers.json_serializer.json_serializer import JsonSerializer
from project_parser.object_converter import refactor_object, restore_object


class TomlSerializer:
    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'w') as outfile:
            outfile.write(TomlSerializer.obj_to_toml(obj))

    def dumps(self, obj):
        return TomlSerializer.obj_to_toml(obj)

    def load(self, fp): # pragma: no cover
        with open(fp, "r") as infile:
            content = infile.read()
        return TomlSerializer.toml_to_obj(content)

    def loads(self, s):
        return TomlSerializer.toml_to_obj(s)

    @staticmethod
    def obj_to_toml(obj):
        ref_obj = refactor_object(obj)
        if type(ref_obj) is int:
            return TomlSerializer.int_to_toml(ref_obj)
        elif type(ref_obj) is float:
            return TomlSerializer.float_to_toml(ref_obj)
        elif type(ref_obj) is bool:
            return TomlSerializer.bool_to_toml(ref_obj)
        elif type(ref_obj) is str:
            return TomlSerializer.str_to_toml(ref_obj)
        elif type(ref_obj) is type(None):
            return TomlSerializer.none_to_toml(ref_obj)
        elif type(ref_obj) is list:
            return TomlSerializer.list_to_toml(ref_obj)
        elif type(ref_obj) is dict:
            return TomlSerializer.dict_to_toml(ref_obj)
        else:
            raise ValueError(f"{type(ref_obj)} isn't supported")

    @staticmethod
    def toml_to_obj(toml_str):
        null = None
        true = True
        false = False
        obj = eval(toml_str)
        return restore_object(obj)

    @staticmethod
    def int_to_toml(obj):
        return str(obj)

    @staticmethod
    def float_to_toml(obj):
        return str(obj)

    @staticmethod
    def bool_to_toml(obj):
        return str(obj).lower()

    @staticmethod
    def str_to_toml(obj):
        obj = obj.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{obj}"'

    @staticmethod
    def none_to_toml(obj):
        return 'null'

    @staticmethod
    def list_to_toml(obj):
        result_str = ''
        for item in obj:
            refactored_item = ''
            if type(item) is int:
                refactored_item += TomlSerializer.int_to_toml(item)
            elif type(item) is float:
                refactored_item += TomlSerializer.float_to_toml(item)
            elif type(item) is bool:
                refactored_item += TomlSerializer.bool_to_toml(item)
            elif type(item) is str:
                refactored_item += TomlSerializer.str_to_toml(item)
            elif type(item) is type(None):
                refactored_item += TomlSerializer.none_to_toml(item)
            elif type(item) in (list, tuple):
                refactored_item += TomlSerializer.list_to_toml(item)
            elif type(item) is dict:
                refactored_item += TomlSerializer.dict_to_toml(item)
            else:
                raise ValueError(f"{type(item)} isn't supported")
            result_str += refactored_item + ", "
        return '[' + result_str[:-2] + ']'

    @staticmethod
    def dict_to_toml(obj):
        result_str = ''
        for key, value in obj.items():
            refactored_item = f'{TomlSerializer.str_to_toml(str(key))}: '
            if type(value) is int:
                refactored_item += TomlSerializer.int_to_toml(obj[key])
            elif type(value) is float:
                refactored_item += TomlSerializer.float_to_toml(obj[key])
            elif type(value) is bool:
                refactored_item += TomlSerializer.bool_to_toml(obj[key])
            elif type(value) is str:
                refactored_item += TomlSerializer.str_to_toml(obj[key])
            elif type(value) is type(None):
                refactored_item += TomlSerializer.none_to_toml(obj[key])
            elif type(value) in (list, tuple):
                refactored_item += TomlSerializer.list_to_toml(obj[key])
            elif type(value) is dict:
                refactored_item += TomlSerializer.dict_to_toml(obj[key])
            else:
                raise ValueError(f"{type(value)} isn't supported")
            result_str += refactored_item + ", "
        return '{' + result_str[:-2] + '}'