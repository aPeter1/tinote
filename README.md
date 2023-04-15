# Tinote

Tinote is a lightweight command-line note-taking tool, designed for quick and easy note management. Keep track of your thoughts, ideas, or reminders directly from the terminal.

## Installation

Install Tinote using pip:

```bash
pip install tinote
```

## Usage

Create a new note:

```bash
ti "a note to remember" -c <optional category> -i <optional importance>
```

List all notes:

```bash
ti list
```

List notes with filters (category or importance):

```bash
ti list -c <category> -i <importance>
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
