![Logo](https://raw.githubusercontent.com/aPeter1/tinote/main/assets/color-logo-no-background.png)

## No Thought Left Behind.

#### Huh, that's a pretty good idea. I should write that down. 

###### [proceeds to lose the paper]

#### Wow, I should write down that task for later in Notepad!

###### [proceeds not to save the file before computer restarts that night]

#### Ugh.

Tinote is light-weight command-line note-taking tool, designed for quick and easy note management. Keep track of your thoughts, ideas, or reminders directly from the terminal.

###### (made entirely for myself, but feel free to use it and contribute!)

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
ti list
```

```output
IDEAS---------------------------------------------------------------------------
[ ] 55 A dating app, but for hamster-owners ONLY
[✔] 58 A sushi company that sell BEEF sushi! :O

VAN-STUFF-----------------------------------------------------------------------
[✔] 55 Fix the latch for the fridge
[ ] 58 Install Solar
    [ ] 60 Install roof-rack, hopefully easy
    [ ] 61 Attach panels
    [ ] 62 Run wiring
```

List notes with filters (category or importance or marked) or higher verbosity:

```bash
ti list -c <category> -i <importance> -m <is marked> -v
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
