import json
import os
from tinote import main


def update(final_version):
    data_file = main.NOTES_FILE

    # Check if the data file exists
    if not os.path.exists(data_file):
        return

    # Load the user's data file
    with open(data_file, 'r') as f:
        data = json.load(f)

    # Get the current version from the data
    current_version = data.get("version", "1.0.x")

    # Define a dictionary of update actions keyed by the version they should be applied to
    update_actions = [
        ("1.1.0", update_1_0_x_to_1_1_x)
    ]

    # Apply the update actions in order
    for version, update_action in update_actions:
        if current_version < version:
            print(f"Updating user data file from {current_version} to {version}")
            data = update_action(data)
            current_version = version

    # Update the data version and save the updated data
    data["version"] = final_version
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)


def update_1_0_x_to_1_1_x(data):
    notes, _, _ = data.get("notes", []), data.get("max_id", 0), data.get("last_category", "unknown")

    for note in notes:
        try:
            note["created_timestamp"] = note["timestamp"]
            note["marked_timestamp"] = None
            note["subs"] = [] if "subs" not in note.keys() else note["subs"]

            del note["timestamp"]
        except KeyError:
            pass

    return data
