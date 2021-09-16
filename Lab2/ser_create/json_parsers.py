import re

key_chars = re.compile(r"[{}\[\],:]")


class json_loader:
    def __init__(self, src, start, end):
        self.src = src
        self.start = start
        self.end = end

    def next_key_char(self):
        if self.start >= self.end:
            raise  ValueError("Unexpected end of string")
        result = key_chars.search(self.src, self.start, self.end)
        if result:
            return result[0], result.start()
        else:
            return ",", self.end

    def load_literal(self, start, end):
        self.start = end
        literal = self.src[start:end].strip()
        if literal.startswith('"'):
            return literal[1:-1]
        elif literal == "true":
            return True
        elif literal == "false":
            return False
        elif literal == "null":
            return None
        else:
            try:
                return int(literal)
            except ValueError:
                return float(literal)

    def load_array(self):
        array = []

        while True:
            try:
                array.append(self.load_value())
            except ValueError:
                pass
            ch, i = self.next_key_char()
            if ch == ",":
                self.start = i + 1
            elif ch == "]":
                self.start = i + 1
                return array
            else:
                raise ValueError("Unexpected key char {} at {}".format(ch, i))

    def load_object(self):
        dct = {}
        
        while True:
            ch, i = self.next_key_char()
            if ch == ":":
                key = self.load_key(self.start, i)
                self.start = i + 1
                try:
                    dct[key] = self.load_value()
                except ValueError:
                    pass
                ch, i = self.next_key_char()
                if ch == ",":
                    self.start = i + 1
                elif ch == "}":
                    self.start = i + 1
                    return dct
                else:
                    raise ValueError("Unexpected key char {} at {}".format(ch, i))
            elif ch == "}":
                self.start = i + 1
                return dct
            else:
                raise ValueError("Unexpected key char {} at {}".format(ch, i))

    def load_key(self, start, end):
        return self.src[start:end].strip()[1:-1]

    def load_value(self):
        ch, i = self.next_key_char()
        if ch == "{":
            self.start = i + 1
            return self.load_object()
        elif ch == "[":
            self.start = i + 1
            return self.load_array()
        elif ch in (",", "}", "]"):
            return self.load_literal(self.start, i)
        else:
            raise ValueError("Unexpected key char {} at {}".format(ch, i))


class json_dumper:
    def __init__(self, indent):
        self.indent = " " * indent
        self.nesting = 0
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
        self.parts.append("null")

    def dump_bool(self, obj):
        self.parts.append("true" if obj else "false")

    def dump_num(self, obj):
        self.parts.append(str(obj))

    def dump_str(self, obj):
        self.parts.extend(('"', obj, '"'))

    def dump_array(self, array):
        if len(array) <= 0:
            self.parts.append("[]")
            return

        self.nesting += 1
        self.parts.append("[")
        for element in array:
            self.parts.extend(("\n", self.indent * self.nesting))
            self.dump_obj(element)
            self.parts.append(",")
        self.parts.pop()
        self.nesting -= 1
        self.parts.extend(("\n", self.indent * self.nesting, "]"))

    def dump_dict(self, dictionary):
        if len(dictionary) <= 0:
            self.parts.append("{}")
            return

        self.nesting += 1
        self.parts.append("{")
        for (key, value) in dictionary.items():
            self.parts.extend(("\n", self.indent * self.nesting))
            self.dump_str(key)
            self.parts.append(" : ")
            self.dump_obj(value)
            self.parts.append(",")
        self.parts.pop()
        self.nesting -= 1
        self.parts.extend(("\n", self.indent * self.nesting, "}"))

    def dump_obj(self, obj):
        self.howdump[type(obj)](obj)


def dumps(obj, indent=4):
    dumper = json_dumper(indent)
    dumper.dump_obj(obj)
    return "".join(dumper.parts)


def loads(src):
    return json_loader(src, 0, len(src)).load_value()
