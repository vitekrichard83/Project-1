# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file static HTML todo list application. No build tools, frameworks, or dependencies.

## Architecture

Everything lives in `index.html`:
- **HTML** — structure (input row + unordered list)
- **CSS** — inline `<style>` block, self-contained styling
- **JS** — inline `<script>` block, vanilla DOM manipulation

There is no server, no bundler, and no external assets. Open `index.html` directly in a browser to run the app.
