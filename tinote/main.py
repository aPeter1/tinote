import json
import argparse
import os
from datetime import datetime
import textwrap


NOTES_FILE = os.path.expanduser("~/.ti_notes.json")


def save_notes(notes, max_id, last_category):
    with open(NOTES_FILE, "w") as f:
        json.dump({"notes": notes, "max_id": max_id, "last_category": last_category}, f, indent=2)


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return [], 0, "unknown"  # Return max_id as 0 for an empty file

    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return [], 0, "unknown"  # Return max_id as 0 for an empty file

        data = json.loads(content)
        notes, max_id, last_category = data.get("notes", []), data.get("max_id", 0), data.get("last_category",
                                                                                              "unknown")
        return notes, max_id, last_category


def create_note(note, category, importance):
    notes, max_id, last_category = load_notes()
    category = last_category if category is None else category

    new_id = max_id + 1

    new_note = {
        "id": new_id,  # Use the new ID
        "note": note,
        "category": category,
        "importance": importance,
        "created_timestamp": datetime.now().isoformat(),
        "marked_timestamp": None,
        "subs": [],
        "checked": False,
    }

    notes.append(new_note)
    save_notes(notes, new_id, category)  # Update max_id

    print("Note added successfully.")


def create_sub_note(note, parent_id, importance):
    notes, max_id, last_category = load_notes()

    for n in notes:
        if n["id"] == parent_id:
            parent_note = n
            break
    else:
        print("Parent does not exist.")
        return

    new_id = max_id + 1

    new_note = {
        "id": new_id,  # Use the new ID
        "parent": parent_id,
        "note": note,
        "category": parent_note["category"],
        "importance": importance,
        "created_timestamp": datetime.now().isoformat(),
        "marked_timestamp": None,
        "checked": False,
    }

    try:
        parent_note["subs"].append(new_note)
    except KeyError:
        parent_note["subs"] = [new_note]

    save_notes(notes, new_id, last_category)

    print("Sub-note added successfully.")


def format_note(note_text, indent):
    bullet_indent = (indent * "\t") + "\t"
    lines = note_text.split("*")
    formatted_lines = [lines[0]] + [f"{bullet_indent}* {line.strip()}" for line in lines[1:]]
    return "\n".join(formatted_lines)


def list_notes(category=None, importance=None, verbose=None, marked=None, unmarked=None):
    notes, _, _ = load_notes()

    if not category:
        sorted_notes = sorted(notes, key=lambda x: x['category'])
    else:
        sorted_notes = [note for note in notes if note['category'] == category]

    def display_notes(notes_list, indent=0):
        for note in notes_list:
            if importance and note["importance"] != importance:
                continue

            if marked is not None and not note["checked"]:
                continue

            if unmarked is not None and note["checked"]:
                continue

            checked_symbol = "[✔]" if note["checked"] else "[ ]"
            importance_symbol = f"[{note['importance']}]" if note["importance"] is not None and verbose else ""
            created_timestamp = f'(Created {note["created_timestamp"]})' if verbose else ""
            marked_timestamp = f'(Mark Updated {note["marked_timestamp"]})' if verbose and note["marked_timestamp"] is not None else ""

            lines = textwrap.wrap(note['note'], width=80 - indent)
            first_line = format_note(lines.pop(0), indent)

            print(
                f"{indent * ' '}{checked_symbol} {note['id']} {first_line} "
                f"{importance_symbol} {created_timestamp} {marked_timestamp}"
            )

            for line in lines:
                print(f"{indent * ' '}   {line}")

            try:
                if note["subs"]:
                    display_notes(note["subs"], indent + 4)
            except KeyError:
                pass

    grouped_notes = {}
    for note in sorted_notes:
        grouped_notes.setdefault(note['category'], []).append(note)

    for category, cat_notes in grouped_notes.items():
        print(f"\n{category.upper()}{'-' * (80 - len(category))}")
        display_notes(cat_notes)


def mark_note(note_id, checked=True):
    notes, max_id, last_category = load_notes()

    for note in notes:
        if note["id"] == note_id:
            note["checked"] = checked
            note["marked_timestamp"] = datetime.now().isoformat()
            save_notes(notes, max_id, last_category)
            print(f"Note {'marked' if checked else 'unmarked'} successfully.")
            return

        for index, sub in enumerate(note["subs"]):
            if sub["id"] == note_id:
                sub["checked"] = checked
                note["marked_timestamp"] = datetime.now().isoformat()
                save_notes(notes, max_id, last_category)
                print(f"Note {'marked' if checked else 'unmarked'} successfully.")
                return
    else:
        print("Invalid note ID.")


def delete_note(note_id):
    notes, max_id, last_category = load_notes()

    for index, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[index]
            save_notes(notes, max_id, last_category)
            print("Note deleted successfully.")
            return

        for sub_index, sub in enumerate(note["subs"]):
            if sub["id"] == note_id:
                del note["subs"][sub_index]
                save_notes(notes, max_id, last_category)
                print("Note deleted successfully.")
                return
    else:
        print("Invalid note ID.")


def clear_notes(category=None):
    notes, max_id, last_category = load_notes()
    if category:
        notes = [note for note in notes if note['category'] != category]
    else:
        notes = []

    save_notes(notes, max_id, last_category)
    if category:
        print(f"Successfully cleared all notes in category '{category}'.")
    else:
        print("Successfully cleared all notes.")


def main():
    parser = argparse.ArgumentParser(description="A command-line tool for taking quick notes.", prog="ti")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Add subparser for 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new note.")
    add_parser.add_argument("note", type=str, help="The content of the note.")
    add_parser.add_argument("category", type=str, nargs="?", default=None,
                            help="Optional category for the note. If none is provided, the last category will be used.")
    add_parser.add_argument("importance", type=int, nargs="?", default=None,
                            help="Optional importance level for the note (integer).")
    add_parser.add_argument("-c", "--category", type=str, default=None,
                            help="Optional category for the note. If none is provided, the last category will be used.",
                            dest="category_keyword")
    add_parser.add_argument("-i", "--importance", type=int, default=None,
                            help="Optional importance level for the note (integer).", dest="importance_keyword")

    sub_parser = subparsers.add_parser('sub', help='Add a sub-note to a note')
    sub_parser.add_argument('parent_id', type=int, help='Parent note ID')
    sub_parser.add_argument('note', type=str, help='Sub-note text')
    sub_parser.add_argument("-i", "--importance", type=int, default=None,
                            help="Optional importance level for the note (integer).")

    # Add subparser for 'list' command
    list_parser = subparsers.add_parser("list", help="List all notes.")
    list_parser.add_argument("-c", "--category", type=str, default=None, help="List notes from a specific category.")
    list_parser.add_argument("-i", "--importance", type=int, default=None,
                             help="List notes with a specific importance level.")
    list_parser.add_argument("-v", "--verbose", action="store_true",
                             help="Show importance and timestamp with each note.")
    list_parser.add_argument("-m", "--marked", action="store_true", default=None,
                             help="Only show marked items")
    list_parser.add_argument("-u", "--unmarked", action="store_true", default=None,
                             help="Only show unmarked items")

    mark_parser = subparsers.add_parser("mark", help="Mark a note as checked or unchecked.")
    mark_parser.add_argument("id", type=int, help="The ID of the note to mark.")
    mark_parser.add_argument("-u", "--uncheck", action="store_true", help="Unmark the note instead of marking it.")

    delete_parser = subparsers.add_parser("delete", help="Delete a note.")
    delete_parser.add_argument("id", type=int, help="The ID of the note to delete.")

    clear_parser = subparsers.add_parser('clear', help='Clear all notes or notes in the specified category')
    clear_parser.add_argument('-c', '--category', type=str, help='Category of notes to clear (optional)')

    args = parser.parse_args()

    if args.subcommand == "add":
        category = args.category_keyword if args.category_keyword is not None else args.category
        importance = args.importance_keyword if args.importance_keyword is not None else args.importance
        create_note(args.note, category, importance)
    elif args.subcommand == "list":
        list_notes(args.category, args.importance, args.verbose, args.marked, args.unmarked)
    elif args.subcommand == "mark":
        mark_note(args.id, not args.uncheck)
    elif args.subcommand == "delete":
        delete_note(args.id)
    elif args.subcommand == 'clear':
        clear_notes(args.category)
    elif args.subcommand == 'sub':
        create_sub_note(args.note, args.parent_id, args.importance)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
