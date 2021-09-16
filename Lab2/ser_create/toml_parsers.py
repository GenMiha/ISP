import re
from functools import reduce

key_chars = re.compile("[\\[=]")
value_chars = re.compile("[\"\n]")


class toml_loader:
    def __init__(self, src, start, end):
        self.src = src
        self.start = start
        self.end = end
        self.root = ({}, False)
        self.current = self.root

    def load_value(self):
        search = value_chars.search(self.src, self.start)
        i = search.start() if search else self.end
        if search and self.src[i] == '"':
            j = self.src.index('"', i + 1)
            self.start = j + 1
            return self.src[i+1:j]

        literal = self.src[self.start:i].strip()
        self.start = i + 1
        if literal == "true":
            return True
        elif literal == "false":
            return False
        elif literal == "":
            return None
        else:
            try:
                return int(literal)
            except ValueError:
                return float(literal)

    def load_loop(self):
        while True:
            search = key_chars.search(self.src, self.start)
            if not search:
                return
            i = search.start()
            ch = self.src[i]
            if ch == "[":
                if self.src[i+1] == "[":
                    is_array = True
                    self.start = i + 2
                else:
                    is_array = False
                    self.start = i + 1
                j = self.src.index("]", self.start)
                path = self.src[self.start:j].split(".")
                self.current = reduce(lambda x, name: x[0].setdefault(name, ({}, is_array)),
                                      path,
                                      self.root)
                if is_array:
                    self.start = j + 3
                else:
                    self.start = j + 2
            else:
                key = self.src[self.start:i].strip()
                self.start = i + 1
                value = self.load_value()
                self.current[0][key] = value

    def restore_table(self, table):
        for (key, value) in table[0].items():
            if type(value) is tuple:
                r = self.restore_table(value)
                table[0][key] = r
        if table[1]:
            return list(table[0].values())
        else:
            return table[0]

    def load_all(self):
        self.load_loop()
        root = self.restore_table(self.root)
        return root["_"]
        


class toml_dumper:
    def __init__(self, indent):
        self.indent = " " * indent
        self.nesting = -1
        self.path = ()
        self.parts = []
        self.howdump = {
            type(None): self.dump_none,
            bool: self.dump_bool,
            int: self.dump_num,
            float: self.dump_num,
            str: self.dump_str,
            list: self.dump_array,
            dict: self.dump_dict,
        }

    def dump_none(self, obj):
        self.parts.append("")

    def dump_bool(self, obj):
        self.parts.append("true" if obj else "false")

    def dump_num(self, obj):
        self.parts.append(str(obj))

    def dump_str(self, obj):
        self.parts.extend(( '"', obj, '"'))

    def dump_table(self, table, is_array):
        path = self.path
        if path:
            self.parts.extend(("\n",
                               self.indent * self.nesting,
                               "[[" if is_array else "[",
                               ".".join(path),
                               "]]" if is_array else "]",
                               "\n"))

        for (key, value) in table:
            if type(value) in (dict, list):
                self.nesting += 1
                self.path = (*path, key)
                self.dump_obj(value)
                self.nesting -= 1
            else:
                if self.path != path:
                    self.path = path
                    self.parts.extend(("\n",
                                       self.indent * self.nesting,
                                       "[[" if is_array else "[",
                                       ".".join(path),
                                       "]]" if is_array else "]",
                                       "\n"))
                self.parts.extend((self.indent * self.nesting, key, " = "))
                self.dump_obj(value)
                self.parts.append("\n")

    def dump_array(self, array):
        self.dump_table(tuple((str(i), array[i]) for i in range(len(array))), True)

    def dump_dict(self, dictionary):
        self.dump_table(dictionary.items(), False)

    def dump_obj(self, obj):
        self.howdump[type(obj)](obj)


def dumps(obj, indent=2):
    dumper = toml_dumper(indent)
    root = { "_": obj}
    dumper.dump_obj(root)
    return "".join(dumper.parts[1:-1])


def loads(src):
    return toml_loader(src, 0, len(src)).load_all()
