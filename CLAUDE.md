# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Scripts

```bash
# Organize Downloads (preview only)
python3 organize_downloads.py --dry-run

# Organize a specific directory
python3 organize_downloads.py --dir /path/to/dir

# Todo list
python3 todo.py add "Task description"
python3 todo.py list
python3 todo.py done <id>
python3 todo.py remove <id>
```

No dependencies to install — both scripts use only the Python standard library.

## Architecture

**`organize_downloads.py`** — Moves top-level files in a directory into `Category/YYYY-MM/` subdirectories based on file extension. Key details:
- `CATEGORIES` dict maps category names to sets of extensions; unrecognized extensions go to `Others/`
- Only top-level files are moved; existing subdirectories are untouched
- Collision handling: appends `_1`, `_2`, etc. to the filename stem if the destination already exists
- `PRIORITY_CATEGORIES` list exists to document intended precedence, but `get_category()` iterates `CATEGORIES` insertion order — if an extension appears in multiple categories, the first match wins

**`todo.py`** — Persists tasks to `todos.json` (next to the script) as a JSON array of `{"id": int, "text": str, "done": bool}`. IDs are assigned as `max(existing ids) + 1` and are never reused after removal.
