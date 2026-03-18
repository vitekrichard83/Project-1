import os
import shutil
from pathlib import Path
from datetime import datetime
import pytest

from organize_downloads import get_category, get_year_month, organize


# --- get_category ---

def test_get_category_images():
    assert get_category(".jpg") == "Images"
    assert get_category(".PNG") == "Images"  # case insensitive

def test_get_category_audio():
    assert get_category(".mp3") == "Audio"

def test_get_category_documents():
    assert get_category(".pdf") == "Documents"

def test_get_category_code():
    assert get_category(".py") == "Code"

def test_get_category_archives():
    assert get_category(".zip") == "Archives"

def test_get_category_unknown():
    assert get_category(".unknownext") == "Others"

def test_get_category_no_extension():
    assert get_category("") == "Others"


# --- get_year_month ---

def test_get_year_month(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello")
    result = get_year_month(f)
    now = datetime.now()
    assert result == now.strftime("%Y-%m")


# --- organize ---

def test_organize_moves_file(tmp_path):
    f = tmp_path / "photo.jpg"
    f.write_text("data")
    organize(tmp_path)
    # After organize, the original path should not exist
    assert not f.exists()
    # A file should be under Images/<YYYY-MM>/
    matches = list((tmp_path / "Images").rglob("photo.jpg"))
    assert len(matches) == 1

def test_organize_dry_run_does_not_move(tmp_path):
    f = tmp_path / "photo.jpg"
    f.write_text("data")
    organize(tmp_path, dry_run=True)
    assert f.exists()
    assert not (tmp_path / "Images").exists()

def test_organize_skips_hidden_files(tmp_path):
    f = tmp_path / ".hidden"
    f.write_text("hidden")
    organize(tmp_path)
    assert f.exists()

def test_organize_skips_subdirectories(tmp_path):
    sub = tmp_path / "SubDir"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested")
    organize(tmp_path)
    assert sub.exists()
    assert (sub / "nested.txt").exists()

def test_organize_collision_handling(tmp_path):
    f1 = tmp_path / "doc.pdf"
    f1.write_text("first")
    organize(tmp_path)
    ym = datetime.now().strftime("%Y-%m")
    dest_dir = tmp_path / "Documents" / ym
    # Place another file with same name back in root
    f2 = tmp_path / "doc.pdf"
    f2.write_text("second")
    organize(tmp_path)
    # Should have doc.pdf and doc_1.pdf
    assert (dest_dir / "doc.pdf").exists()
    assert (dest_dir / "doc_1.pdf").exists()

def test_organize_nonexistent_directory(capsys):
    organize(Path("/nonexistent/path/xyz"))
    captured = capsys.readouterr()
    assert "not found" in captured.out

def test_organize_unknown_extension(tmp_path):
    f = tmp_path / "file.unknownext"
    f.write_text("data")
    organize(tmp_path)
    assert not f.exists()
    matches = list((tmp_path / "Others").rglob("file.unknownext"))
    assert len(matches) == 1
