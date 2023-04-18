![Logo](https://raw.githubusercontent.com/aPeter1/tinote/main/assets/color-logo-no-background.png)

Tinote is light-weight command-line note-taking tool, designed for quick and easy note management. Keep track of your thoughts, ideas, or reminders directly from the terminal.

## Installation

Install Tinote using pip:

```bash
pip install tinote
```

## Usage

Create a new note (if no category is provided, the last category will be used):

```bash
ti add "a note to remember" <optional category> <optional importance>
```

List all notes (verbose list will include importance and timestamp):

```bash
ti list [-v]
```

List notes with filters (category or importance):

```bash
ti list -c <category> -i <importance>
```

Add a sub-note to a note (currently only supports one level)

```bash
ti sub <parent_id> "Text of your sub-note" -i <importance>
```

Mark a note as checked/unchecked:

```bash
ti mark <note_id>
```

Delete a note:

```bash
ti delete <note_id>
```

Clear all notes or notes within a specified category:

```bash
ti clear
ti clear -c <category>
```

## Features

- Create and manage notes with optional categories and importance levels
- List notes, with optional filters for categories and importance
- Easily mark notes as checked/unchecked
- Delete notes using their ID
- Clear all notes or notes within a specified category
- Automatically saves notes to a local JSON file for persistence

## License

MIT License
