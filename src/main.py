import json
import argparse
import os
from datetime import datetime

NOTES_FILE = os.path.expanduser("~/.ti_notes.json")


def save_notes(notes, max_id):
    with open(NOTES_FILE, "w") as f:
        json.dump({"notes": notes, "max_id": max_id}, f, indent=2)


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return [], 0  # Return max_id as 0 for an empty file

    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return [], 0  # Return max_id as 0 for an empty file

        data = json.loads(content)
        notes, max_id = data.get("notes", []), data.get("max_id", 0)
        return notes, max_id


def create_note(note, category, importance):
    notes, max_id = load_notes()
    new_id = max_id + 1

    new_note = {
        "id": new_id,  # Use the new ID
        "note": note,
        "category": category,
        "importance": importance,
        "timestamp": datetime.now().isoformat(),
        "checked": False,
    }

    notes.append(new_note)
    save_notes(notes, new_id)  # Update max_id

    print("Note added successfully.")


def format_note(note_text):
    lines = note_text.split("*")
    formatted_lines = [lines[0]] + [f"\t* {line.strip()}" for line in lines[1:]]
    return "\n".join(formatted_lines)


def list_notes(category=None, importance=None):
    notes, _ = load_notes()
    if not notes:
        print("No notes found.")
        return

    if category or importance is not None:
        filtered_notes = [note for note in notes if (not category or note["category"] == category) and (importance is None or note["importance"] == importance)]
        if not filtered_notes:
            print("No notes found matching the given filters.")
            return

        for note in filtered_notes:
            checkbox = "[x]" if note["checked"] else "[ ]"
            formatted_note = format_note(note["note"])
            print(f"{note['id']}. {checkbox} {formatted_note} (Category: {note['category']}, Importance: {note['importance']}, Timestamp: {note['timestamp']})")
    else:
        grouped_notes = {category: [note for note in notes if note["category"] == category] for category in set(note["category"] for note in notes)}

        for category, category_notes in grouped_notes.items():
            print(f"Category: {category or 'Uncategorized'}")
            for note in category_notes:
                checkbox = "[x]" if note["checked"] else "[ ]"
                formatted_note = format_note(note["note"])
                print(f"  {note['id']}. {checkbox} {formatted_note} (Importance: {note['importance']}, Timestamp: {note['timestamp']})")
            print()


def mark_note(note_id, checked=True):
    notes, max_id = load_notes()

    for note in notes:
        if note["id"] == note_id:
            note["checked"] = checked
            save_notes(notes, max_id)
            print(f"Note {'marked' if checked else 'unmarked'} successfully.")
            break
    else:
        print("Invalid note ID.")


def delete_note(note_id):
    notes, max_id = load_notes()

    for index, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[index]
            save_notes(notes, max_id)
            print("Note deleted successfully.")
            break
    else:
        print("Invalid note ID.")


def main():
    parser = argparse.ArgumentParser(description="A command-line tool for taking quick notes.", prog="ti")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Add subparser for 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new note.")
    add_parser.add_argument("note", type=str, help="The content of the note.")
    add_parser.add_argument("-c", "--category", type=str, default=None, help="Optional category for the note.")
    add_parser.add_argument("-i", "--importance", type=int, default=None, help="Optional importance level for the note (integer).")

    # Add subparser for 'list' command
    list_parser = subparsers.add_parser("list", help="List all notes.")
    list_parser.add_argument("-c", "--category", type=str, default=None, help="List notes from a specific category.")
    list_parser.add_argument("-i", "--importance", type=int, default=None, help="List notes with a specific importance level.")

    mark_parser = subparsers.add_parser("mark", help="Mark a note as checked or unchecked.")
    mark_parser.add_argument("id", type=int, help="The ID of the note to mark.")
    mark_parser.add_argument("-u", "--uncheck", action="store_true", help="Unmark the note instead of marking it.")

    delete_parser = subparsers.add_parser("delete", help="Delete a note.")
    delete_parser.add_argument("id", type=int, help="The ID of the note to delete.")

    args = parser.parse_args()

    if args.subcommand == "add":
        create_note(args.note, args.category, args.importance)
    elif args.subcommand == "list":
        list_notes(args.category, args.importance)
    elif args.subcommand == "mark":
        mark_note(args.id, not args.uncheck)
    elif args.subcommand == "delete":
        delete_note(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
