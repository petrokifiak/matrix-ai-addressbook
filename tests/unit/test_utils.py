import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')),
)

from src.utils import parse_input


class TestUtils(unittest.TestCase):
    def test_parse_input_simple(self):
        cmd, args = parse_input("hello")
        self.assertEqual(cmd, "hello")
        self.assertEqual(args, [])

    def test_parse_input_with_args(self):
        cmd, args = parse_input("add John 0501234567")
        self.assertEqual(cmd, "add")
        self.assertEqual(args, ["John", "0501234567"])

    def test_parse_input_with_quotes(self):
        cmd, args = parse_input('add-note "My Title" "Some content here"')
        self.assertEqual(cmd, "add-note")
        self.assertEqual(args, ["My Title", "Some content here"])

    def test_parse_input_with_single_quotes(self):
        cmd, args = parse_input("show-birthday 'Mark Zuckerberg'")
        self.assertEqual(cmd, "show-birthday")
        self.assertEqual(args, ["Mark Zuckerberg"])

    def test_parse_input_unbalanced_quotes(self):
        # Fallback to standard split if quotes are unbalanced
        cmd, args = parse_input('add-note "My Title')
        self.assertEqual(cmd, "add-note")
        self.assertEqual(args, ['"My', 'Title'])

    def test_parse_input_empty(self):
        cmd, args = parse_input("   ")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])

    def test_parse_input_capitalization(self):
        cmd, args = parse_input(" ADD John ")
        self.assertEqual(cmd, "add")
        self.assertEqual(args, ["John"])


if __name__ == "__main__":
    unittest.main()
