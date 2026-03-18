#!/usr/bin/env node
/**
 * organize-downloads - Organize files in ~/Downloads into categorized subdirectories.
 *
 * Usage:
 *   npm start -- [--dry-run] [--dir PATH]
 *
 * Options:
 *   --dry-run    Show what would happen without moving any files
 *   --dir PATH   Specify a directory to organize (default: ~/Downloads)
 */

import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { Command } from "commander";

// ---------------------------------------------------------------------------
// Extension constants per category
// ---------------------------------------------------------------------------

const IMAGE_EXTENSIONS = [
  ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
  ".tiff", ".tif", ".ico", ".heic", ".heif", ".raw", ".cr2",
  ".nef", ".orf", ".arw",
] as const;

const VIDEO_EXTENSIONS = [
  ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
  ".m4v", ".mpg", ".mpeg", ".3gp", ".ogv", ".ts", ".vob",
] as const;

const AUDIO_EXTENSIONS = [
  ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
  ".opus", ".aiff", ".mid", ".midi",
] as const;

const DOCUMENT_EXTENSIONS = [
  ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md",
  ".tex", ".pages", ".xlsx", ".xls", ".ods", ".csv",
  ".pptx", ".ppt", ".odp", ".key", ".epub", ".mobi",
] as const;

const ARCHIVE_EXTENSIONS = [
  ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
  ".tgz", ".tbz2", ".zst", ".lz4", ".iso", ".dmg",
] as const;

const CODE_EXTENSIONS = [
  ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm",
  ".css", ".scss", ".sass", ".sh", ".bash", ".zsh",
  ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h",
  ".hpp", ".cs", ".php", ".swift", ".kt", ".r",
  ".sql", ".json", ".yaml", ".yml", ".toml", ".xml",
  ".lua", ".pl", ".vim", ".dart",
] as const;

const EXECUTABLE_EXTENSIONS = [
  ".exe", ".msi", ".deb", ".rpm", ".appimage", ".apk",
  ".snap", ".flatpakref", ".pkg", ".dmg", ".run",
] as const;

const FONT_EXTENSIONS = [
  ".ttf", ".otf", ".woff", ".woff2", ".eot",
] as const;

const EBOOK_EXTENSIONS = [
  ".epub", ".mobi", ".azw", ".azw3", ".fb2",
] as const;

const TORRENT_EXTENSIONS = [
  ".torrent", ".magnet",
] as const;

// ---------------------------------------------------------------------------
// Category map built from the constants above
// ---------------------------------------------------------------------------

const CATEGORIES: Record<string, ReadonlySet<string>> = {
  Images:      new Set(IMAGE_EXTENSIONS),
  Videos:      new Set(VIDEO_EXTENSIONS),
  Audio:       new Set(AUDIO_EXTENSIONS),
  Documents:   new Set(DOCUMENT_EXTENSIONS),
  Archives:    new Set(ARCHIVE_EXTENSIONS),
  Code:        new Set(CODE_EXTENSIONS),
  Executables: new Set(EXECUTABLE_EXTENSIONS),
  Fonts:       new Set(FONT_EXTENSIONS),
  Ebooks:      new Set(EBOOK_EXTENSIONS),
  Torrents:    new Set(TORRENT_EXTENSIONS),
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getCategory(ext: string): string {
  const normalized = ext.toLowerCase();
  for (const [category, extensions] of Object.entries(CATEGORIES)) {
    if (extensions.has(normalized)) {
      return category;
    }
  }
  return "Others";
}

function getYearMonth(filePath: string): string {
  const stat = fs.statSync(filePath);
  const dt = new Date(stat.mtimeMs);
  const year = dt.getFullYear();
  const month = String(dt.getMonth() + 1).padStart(2, "0");
  return `${year}-${month}`;
}

// ---------------------------------------------------------------------------
// Core organizer
// ---------------------------------------------------------------------------

function organize(directory: string, dryRun: boolean): void {
  if (!fs.existsSync(directory)) {
    console.log(`Directory not found: ${directory}`);
    return;
  }

  let moved = 0;
  let skipped = 0;

  const entries = fs.readdirSync(directory).sort();

  for (const name of entries) {
    const itemPath = path.join(directory, name);
    const stat = fs.statSync(itemPath);

    if (stat.isDirectory() || name.startsWith(".")) {
      skipped++;
      continue;
    }

    const ext = path.extname(name);
    const stem = path.basename(name, ext);
    const category = getCategory(ext);
    const yearMonth = getYearMonth(itemPath);
    const destDir = path.join(directory, category, yearMonth);

    let destPath = path.join(destDir, name);
    let counter = 1;
    while (fs.existsSync(destPath)) {
      destPath = path.join(destDir, `${stem}_${counter}${ext}`);
      counter++;
    }

    const relDest = path.relative(directory, destPath);
    const prefix = dryRun ? "[DRY RUN] " : "";
    console.log(`${prefix}Move  ${name}`);
    console.log(`         -> ${relDest}`);

    if (!dryRun) {
      fs.mkdirSync(destDir, { recursive: true });
      fs.renameSync(itemPath, destPath);
    }

    moved++;
  }

  const prefix = dryRun ? "[DRY RUN] " : "";
  console.log(
    `\n${prefix}Done. ${moved} file(s) organized, ${skipped} item(s) skipped.`
  );
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

const program = new Command();

program
  .name("organize-downloads")
  .description("Organize ~/Downloads into categorized subdirectories.")
  .option("--dry-run", "Preview changes without moving any files.", false)
  .option(
    "--dir <path>",
    "Directory to organize (default: ~/Downloads).",
    path.join(os.homedir(), "Downloads")
  )
  .action((options: { dryRun: boolean; dir: string }) => {
    console.log(`Organizing: ${options.dir}`);
    console.log(`Dry run:    ${options.dryRun}\n`);
    organize(options.dir, options.dryRun);
  });

program.parse(process.argv);
