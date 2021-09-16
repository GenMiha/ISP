import re

skips = re.compile(r"[^ ]")


class yaml_loader:
    def __init__(self, src, start, end):
        self.src = src
        self.start = start
        self.end = end
        self.nesting = 0

    def load_value(self):
        if self.src.startswith('"', self.start):
            start = self.start + 1
            end = self.src.index('"', start)
            self.start = end + 2 # skip quote and '\n'
            return self.src[start:end]
        elif self.src.startswith("[]", self.start):
            self.start += 3
            return []
        elif self.src.startswith("{}", self.start):
            self.start += 3
            return {}
        elif self.src.startswith("true", self.start):
            self.start += 5
            return True
        elif self.src.startswith("false", self.start):
            self.start += 6
            return False
        elif self.src.startswith("null", self.start):
            self.start += 5
            return None
        else:
            start = self.start
            end = self.src.find('\n', self.start)
            if end < 0:
                end = self.end
            literal = self.src[start:end]
            try:
                tmp = int(literal)
            except ValueError:
                tmp = float(literal)
            self.start = end + 1
            return tmp

    def load_array(self, lst):
        while True:
            self.start +=  2 # skip '- '
            self.nesting += 1
            lst.append(self.load_smth())
            self.nesting -= 1

            search = skips.search(self.src, self.start)
            if not search:
                return
            nesting = (search.start() - self.start) // 2
            if nesting < self.nesting or self.src[search.start()] != "-":
                return
            self.start = search.start()

    def load_dict(self, dct):
        while True:
            i = self.src.index(":", self.start)
            key = self.src[self.start:i]
            ch = self.src[i+1]
            self.start = i + 2 # skip ': ' or ':\n'
            if ch == " ":
                dct[key] = self.load_value()
            else:
                search = skips.search(self.src, self.start)
                nesting = (search.start() - self.start) // 2
                self.start = search.start()
                if nesting > self.nesting:
                    tmp = {}
                    self.nesting += 1
                    self.load_dict(tmp)
                    self.nesting -= 1
                else: # it is list
                    tmp = []
                    self.load_array(tmp)
                dct[key] = tmp

            search = skips.search(self.src, self.start)
            if not search:
                return
            nesting = (search.start() - self.start) // 2
            if nesting < self.nesting:
                return
            self.start = search.start()

    def load_smth(self):
        if self.src.startswith("- ", self.start):
            tmp = []
            self.load_array(tmp)
            return tmp
        else:
            try:
                return self.load_value()
            except ValueError:
                tmp = {}
                self.load_dict(tmp)
                return tmp


class yaml_dumper:
    def __init__(self):
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

        for element in array:
            self.nesting += 1
            self.parts.append("- ")
            self.dump_obj(element)
            self.nesting -= 1
            self.parts.extend(("\n", "  " * self.nesting))

        self.parts.pop()
        self.parts.pop()

    def dump_dict(self, dictionary):
        if len(dictionary) <= 0:
            self.parts.append("{}")
            return

        for (key, value) in dictionary.items():
            self.parts.extend((key, ":"))
            if type(value) is dict:
                self.nesting += 1
            if type(value) in (dict, list) and len(value) > 0:
                self.parts.extend(("\n", "  " * self.nesting))
            else:
                self.parts.append(" ")
            self.dump_obj(value)
            if type(value) is dict:
                self.nesting -= 1
            self.parts.extend(("\n", "  " * self.nesting))

        self.parts.pop()
        self.parts.pop()

    def dump_obj(self, obj):
        self.howdump[type(obj)](obj)


def dumps(obj):
    dumper = yaml_dumper()
    dumper.dump_obj(obj)
    return "".join(dumper.parts)


def loads(src):
    return yaml_loader(src, 0, len(src)).load_smth()
