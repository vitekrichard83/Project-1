#!/usr/bin/env python3
"""Simple CLI todo list manager."""

import argparse
import json
import os

TODO_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []


def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def cmd_add(text):
    todos = load_todos()
    next_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": next_id, "text": text, "done": False})
    save_todos(todos)
    print(f"Added [{next_id}]: {text}")


def cmd_list(todos=None):
    if todos is None:
        todos = load_todos()
    if not todos:
        print("No tasks.")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        print(f"[{status}] {t['id']}. {t['text']}")


def cmd_done(task_id):
    todos = load_todos()
    for t in todos:
        if t["id"] == task_id:
            t["done"] = True
            save_todos(todos)
            print(f"Done [{task_id}]: {t['text']}")
            return
    print(f"Task {task_id} not found.")


def cmd_remove(task_id):
    todos = load_todos()
    remaining = [t for t in todos if t["id"] != task_id]
    if len(remaining) == len(todos):
        print(f"Task {task_id} not found.")
        return
    save_todos(remaining)
    print(f"Removed task {task_id}.")


def main():
    parser = argparse.ArgumentParser(description="Simple todo list")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.text)
    elif args.command == "list":
        cmd_list()
    elif args.command == "done":
        cmd_done(args.id)
    elif args.command == "remove":
        cmd_remove(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
