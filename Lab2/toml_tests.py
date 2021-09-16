import unittest
from ser_create import my_dump
from ser_create import my_load
from ser_create.toml_serializer import TomlSerializer
import test_examples as te

toml = TomlSerializer()


class TestingObjects(unittest.TestCase):
    def tearDown(self):
        dumper = toml.dumps(self.tested_obj)
        self.loader = toml.loads(dumper)
        self.assertTrue(self.loader == self.tested_obj)

    def test_none(self):
        self.tested_obj = None

    def test_bool_True(self):
        self.tested_obj = True

    def test_bool_False(self):
        self.tested_obj = False

    def test_int(self):
        self.tested_obj = 323464

    def test_float(self):
        self.tested_obj = 3.14159265359

    def test_complex(self):
        self.tested_obj = complex(1, 2)

    def test_str(self):
        self.tested_obj = "Hello from test"

    def test_list(self):
        self.tested_obj = [1, 2, 3, 4, 5]

    def test_tuple(self):
        self.tested_obj = (1, 2, 3, 4, 5)

    def test_range(self):
        self.tested_obj = range(1, 5, 1)

    def test_bytes(self):
        self.tested_obj = bytes.fromhex("d0 9f d1 80 d0 b8 d0 b2 d0 b5 d1 82")

    def test_bytearray(self):
        self.tested_obj = bytes.fromhex("d0 a2 d0 b5 d1 81 d1 82 d0 b8 d0 bc")

    def test_set(self):
        self.tested_obj = {1, 2, 3, 4, 5}

    def test_frozenset(self):
        self.tested_obj = frozenset({1, 2, 3, 4, 5})

    def test_dict(self):
        self.tested_obj = {"a": 1, "b": 2, "c": 3}


class TestingFunctions(unittest.TestCase):
    def test_func_pass(self):
        tested_obj = te.func_pass
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(), loader())

    def test_func_add_ten(self):
        tested_obj = te.func_add_ten
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(10), loader(10))

    def test_func_with_recursion(self):
        tested_obj = te.func_with_recursion
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(5), loader(5))

    def test_func_with_import(self):
        tested_obj = te.func_with_import
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(0), loader(0))

    def test_func_with_globals(self):
        tested_obj = te.func_with_globals
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(), loader())

    def test_func_with_func(self):
        tested_obj = te.func_with_func
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(), loader())

    def test_func_with_closure(self):
        tested_obj = te.func_with_closure()
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(
            tested_obj.__closure__[0].cell_contents, loader.__closure__[0].cell_contents
        )

    def test_func_decorator(self):
        tested_obj = te.check_decorator
        dumper = toml.dumps(tested_obj)
        loader = toml.loads(dumper)
        self.assertEqual(tested_obj.__code__, loader.__code__)
        self.assertEqual(tested_obj(), loader())


if __name__ == "__main__":
    unittest.main()