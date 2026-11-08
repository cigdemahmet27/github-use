import unittest

from todo import add, complete, format_todos


class TestTodo(unittest.TestCase):
    def test_add(self):
        todos = add([], "buy milk")
        self.assertEqual(todos, [{"text": "buy milk", "done": False}])

    def test_complete(self):
        todos = complete(add([], "buy milk"), 0)
        self.assertTrue(todos[0]["done"])

    def test_format_empty(self):
        self.assertEqual(format_todos([]), "Nothing to do!")

    def test_format(self):
        todos = complete(add(add([], "a"), "b"), 0)
        self.assertEqual(format_todos(todos), "1. [x] a\n2. [ ] b")


if __name__ == "__main__":
    unittest.main()
