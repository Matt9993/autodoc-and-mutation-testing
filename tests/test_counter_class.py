import unittest
from src.counter_class import Counter


class TestCounters(unittest.TestCase):

    def setUp(self) -> None:
        self.counter_object = Counter()

    def test_add_value_int(self) -> None:
        self.counter_object.add(5)
        self.assertEqual(self.counter_object._value, 5)

    def test_add_value_strint(self) -> None:
        with self.assertRaises(TypeError):
            self.counter_object.add("hello world")

    def test_remove_value(self) -> None:
        self.counter_object.add(5)
        self.counter_object.remove(3)
        self.assertEqual(self.counter_object._value, 2)

    def test_remove_value_strint(self) -> None:
        with self.assertRaises(TypeError):
            self.counter_object.remove("hello world")

    def test_clear_value(self) -> None:
        self.counter_object.clear()
        self.assertEqual(self.counter_object._value, 0)

    def tearDown(self) -> None:
        self.counter_object = None
