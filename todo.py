"""A tiny to-do list app, used as a playground for learning Git and GitHub."""

import json
import sys
from pathlib import Path

__version__ = "0.1.0"

DATA_FILE = Path("todos.json")


def load(path=DATA_FILE):
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save(todos, path=DATA_FILE):
    path.write_text(json.dumps(todos, indent=2))


def add(todos, text):
    todos.append({"text": text, "done": False})
    return todos


def complete(todos, index):
    todos[index]["done"] = True
    return todos

def remove(todos, index):
    todos.pop(index)
    return todos


def format_todos(todos):
    if not todos:
        return "Nothing to do!"
    lines = []
    for i, t in enumerate(todos, start=1):
        mark = "x" if t["done"] else " "
        lines.append(f"{i}. [{mark}] {t['text']}")
    return "\n".join(lines)


def main(argv):
    todos = load()
    if len(argv) < 2 or argv[1] == "list":
        print(format_todos(todos))
    elif argv[1] == "add":
        save(add(todos, " ".join(argv[2:])))
        print("Added.")
    elif argv[1] == "done":
        save(complete(todos, int(argv[2]) - 1))
        print("Marked as done.")
    elif argv[1] == "remove":
        save(remove(todos, int(argv[2]) - 1))
        print("Removed.")
    elif argv[1] == "version":
        print(__version__)
    else:
        print("Usage: python todo.py [list | add <text> | done <number>| remove <number> | version]")


if __name__ == "__main__":
    main(sys.argv)
