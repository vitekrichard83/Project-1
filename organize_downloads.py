#!/usr/bin/env python3
"""
organize_downloads.py - Organize files in ~/Downloads into categorized subdirectories.

Usage:
    python3 organize_downloads.py [--dry-run] [--dir PATH]

Options:
    --dry-run    Show what would happen without moving any files
    --dir PATH   Specify a directory to organize (default: ~/Downloads)
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# File type categories mapped to their extensions
CATEGORIES = {
    "Images":       {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
                     ".tiff", ".tif", ".ico", ".heic", ".heif", ".raw", ".cr2",
                     ".nef", ".orf", ".arw"},
    "Videos":       {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
                     ".m4v", ".mpg", ".mpeg", ".3gp", ".ogv", ".ts", ".vob"},
    "Audio":        {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
                     ".opus", ".aiff", ".mid", ".midi"},
    "Documents":    {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md",
                     ".tex", ".pages", ".xlsx", ".xls", ".ods", ".csv",
                     ".pptx", ".ppt", ".odp", ".key", ".epub", ".mobi"},
    "Archives":     {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
                     ".tgz", ".tbz2", ".zst", ".lz4", ".iso", ".dmg"},
    "Code":         {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm",
                     ".css", ".scss", ".sass", ".sh", ".bash", ".zsh",
                     ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h",
                     ".hpp", ".cs", ".php", ".swift", ".kt", ".r",
                     ".sql", ".json", ".yaml", ".yml", ".toml", ".xml",
                     ".lua", ".pl", ".vim", ".dart"},
    "Executables":  {".exe", ".msi", ".deb", ".rpm", ".AppImage", ".apk",
                     ".snap", ".flatpakref", ".pkg", ".dmg", ".run"},
    "Fonts":        {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Ebooks":       {".epub", ".mobi", ".azw", ".azw3", ".fb2"},
    "Torrents":     {".torrent", ".magnet"},
}

# Extensions that should stay in Documents (override Ebooks category collision)
PRIORITY_CATEGORIES = ["Executables", "Torrents", "Archives", "Fonts",
                        "Ebooks", "Audio", "Video", "Images", "Code", "Documents"]


def get_category(suffix: str) -> str:
    """Return the category name for a given file extension."""
    suffix = suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def get_year_month(path: Path) -> str:
    """Return a YYYY-MM string from the file's modification time."""
    mtime = path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime("%Y-%m")


def organize(directory: Path, dry_run: bool = False) -> None:
    """
    Organize files in *directory* into category/year-month subdirectories.

    Only top-level files are moved; existing subdirectories are left intact.
    """
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return

    moved = 0
    skipped = 0

    for item in sorted(directory.iterdir()):
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith("."):
            skipped += 1
            continue

        category = get_category(item.suffix)
        year_month = get_year_month(item)
        dest_dir = directory / category / year_month
        dest = dest_dir / item.name

        # Avoid collision: append a counter if target already exists
        counter = 1
        while dest.exists():
            stem = item.stem
            dest = dest_dir / f"{stem}_{counter}{item.suffix}"
            counter += 1

        print(f"{'[DRY RUN] ' if dry_run else ''}Move  {item.name}")
        print(f"         -> {dest.relative_to(directory)}")

        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), dest)

        moved += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Done. "
          f"{moved} file(s) organized, {skipped} item(s) skipped.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize ~/Downloads into categorized subdirectories."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving any files.",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path.home() / "Downloads",
        metavar="PATH",
        help="Directory to organize (default: ~/Downloads).",
    )
    args = parser.parse_args()

    print(f"Organizing: {args.dir}")
    print(f"Dry run:    {args.dry_run}\n")
    organize(args.dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
