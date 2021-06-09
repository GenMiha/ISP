from project_parser.object_converter import refactor_object, restore_object


class YamlSerializer:
    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'w') as outfile:
            outfile.write(YamlSerializer.obj_to_yaml(obj))

    def dumps(self, obj):
        return YamlSerializer.obj_to_yaml(obj)

    def load(self, fp): # pragma: no cover
        with open(fp, "r") as infile:
            content = infile.read()
        return YamlSerializer.yaml_to_obj(content)

    def loads(self, s):
        return YamlSerializer.yaml_to_obj(s)

    @staticmethod
    def obj_to_yaml(obj):
        ref_obj = refactor_object(obj)
        if type(ref_obj) is int:
            return YamlSerializer.int_to_yaml(ref_obj)
        elif type(ref_obj) is float:
            return YamlSerializer.float_to_yaml(ref_obj)
        elif type(ref_obj) is bool:
            return YamlSerializer.bool_to_yaml(ref_obj)
        elif type(ref_obj) is str:
            return YamlSerializer.str_to_yaml(ref_obj)
        elif type(ref_obj) is type(None):
            return YamlSerializer.none_to_yaml(ref_obj)
        elif type(ref_obj) is list:
            return YamlSerializer.list_to_yaml(ref_obj)
        elif type(ref_obj) is dict:
            return YamlSerializer.dict_to_yaml(ref_obj)
        else:
            raise ValueError(f"{type(ref_obj)} isn't supported")

    @staticmethod
    def yaml_to_obj(yaml_str):
        null = None
        true = True
        false = False
        obj = eval(yaml_str)
        return restore_object(obj)

    @staticmethod
    def int_to_yaml(obj):
        return str(obj)

    @staticmethod
    def float_to_yaml(obj):
        return str(obj)

    @staticmethod
    def bool_to_yaml(obj):
        return str(obj).lower()

    @staticmethod
    def str_to_yaml(obj):
        obj = obj.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{obj}"'

    @staticmethod
    def none_to_yaml(obj):
        return 'null'

    @staticmethod
    def list_to_yaml(obj):
        result_str = ''
        for item in obj:
            refactored_item = ''
            if type(item) is int:
                refactored_item += YamlSerializer.int_to_yaml(item)
            elif type(item) is float:
                refactored_item += YamlSerializer.float_to_yaml(item)
            elif type(item) is bool:
                refactored_item += YamlSerializer.bool_to_yaml(item)
            elif type(item) is str:
                refactored_item += YamlSerializer.str_to_yaml(item)
            elif type(item) is type(None):
                refactored_item += YamlSerializer.none_to_yaml(item)
            elif type(item) in (list, tuple):
                refactored_item += YamlSerializer.list_to_yaml(item)
            elif type(item) is dict:
                refactored_item += YamlSerializer.dict_to_yaml(item)
            else:
                raise ValueError(f"{type(item)} isn't supported")
            result_str += refactored_item + ", "
        return '[' + result_str[:-2] + ']'

    @staticmethod
    def dict_to_yaml(obj):
        result_str = ''
        for key, value in obj.items():
            refactored_item = f'{YamlSerializer.str_to_yaml(str(key))}: '
            if type(value) is int:
                refactored_item += YamlSerializer.int_to_yaml(obj[key])
            elif type(value) is float:
                refactored_item += YamlSerializer.float_to_yaml(obj[key])
            elif type(value) is bool:
                refactored_item += YamlSerializer.bool_to_yaml(obj[key])
            elif type(value) is str:
                refactored_item += YamlSerializer.str_to_yaml(obj[key])
            elif type(value) is type(None):
                refactored_item += YamlSerializer.none_to_yaml(obj[key])
            elif type(value) in (list, tuple):
                refactored_item += YamlSerializer.list_to_yaml(obj[key])
            elif type(value) is dict:
                refactored_item += YamlSerializer.dict_to_yaml(obj[key])
            else:
                raise ValueError(f"{type(value)} isn't supported")
            result_str += refactored_item + ", "
        return '{' + result_str[:-2] + '}'