from datetime import datetime
import json

blue, reset, green, red, yellow = "\033[94m", "\033[0m", "\033[92m", "\033[91m", "\033[93m"


class Note:
    """
    Represents a note object.

    Attributes:
        id (int): The unique identifier for the note.
        text (str): The content of the note.
        tags (set): The set of tags associated with the note.
        creation_date (datetime): The date and time when the note was created.

    Methods:
        modify(new_text): Modifies the text content of the note.
        set_tags(tags): Sets the tags for the note.
        to_dict(): Converts the note object to a dictionary.
        from_dict(data): Creates a note object from a dictionary.
    """

    _last_id = 0

    def __init__(self, text, tags=None):
        """
        Initialize a Note object.
        """
        Note._last_id += 1
        self.id = Note._last_id
        self.text = text
        self.tags = set(tags) if tags else set()
        self.creation_date = datetime.today()

    def modify(self, new_text):
        """
        Modify the text content of the note.
        """
        self.text = new_text

    def set_tags(self, tags):
        """
        Set the tags for the note.
        """

        for tag in tags:
            self.tags = set(tags)

    def to_dict(self):
        """
        Convert the note object to a dictionary.
        """
        return {
            "id": self.id,
            "text": self.text,
            "tags": list(self.tags),
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def from_dict(data):
        """
        Create a note object from a dictionary.
        """
        note = Note(data["text"], data["tags"])
        note.id = data["id"]
        note.creation_date = datetime.strptime(
            data["creation_date"], "%Y-%m-%d %H:%M:%S"
        )
        return note

    def __repr__(self):
        """
        Return a string representation of the note.
        """
        return f'Note(id={self.id}, text="{self.text}", tags={self.tags}, creation_date={self.creation_date})'


class Notebook:
    """
    Represents a collection of notes.

    Attributes:
        notes (list): A list of Note objects.

    Methods:
        add_note(text, tags): Adds a new note to the notebook.
        find_notes(tags, text): Finds notes based on tags and text content.
        _find_note_by_id(note_id): Finds a note by its ID (internal method).
        modify_note(note_id, new_text): Modifies the text content of a note.
        modify_tags(note_id, new_tags): Modifies the tags of a note.
        delete_note(note_id): Deletes a note by its ID.
        find_note_by_id(note_id): Finds a note by its ID.
        save_to_file(file_name): Saves the notebook to a JSON file.
        load_from_file(file_name): Loads notes from a JSON file into the notebook.
    """
    def __init__(self):
        """
        Initialize a Notebook object.
        """
        self.notes = []

    def add_note(self, text, tags=None):
        """
        Adds a new note to the notebook.
        """
        self.notes.append(Note(text, tags))
        self.save_to_file("notes.json")

    def find_notes(self, tags=None, text=None):
        """
        Finds notes based on tags and text content.
        """
        found_notes = self.notes

        if tags:
            found_notes = [
                note for note in found_notes if any(tag in note.tags for tag in tags)
            ]

        if text:
            found_notes = [note for note in found_notes if text in note.text]

        return found_notes

    def _find_note_by_id(self, note_id):
        """
        Finds a note by its ID (internal method).
        """
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def modify_note(self, note_id, new_text):
        """
        Modifies the text content of a note.
        """
        for note in self.notes:
            if note.id == note_id:
                if new_text == "clear":
                    new_text = ""

                note.modify(new_text)
                print(
                    f"{green}Text of the Note with ID {note_id} has been modified.{reset}"
                )
                self.save_to_file("notes.json")
                break

    def modify_tags(self, note_id, new_tags):
        """
        Modifies the tags of a note.
        """
        for note in self.notes:
            if note.id == note_id:
                if new_tags == ["clear"]:
                    note.set_tags(set())
                    print(
                        f"{green}All tags of the Note with ID {note_id} have been cleared.{reset}"
                    )
                else:
                    note.set_tags(new_tags)
                    print(
                        f"{green}Tags of the Note with ID {note_id} has been modified.{reset}\n"
                    )

        self.save_to_file("notes.json")

    def delete_note(self, note_id):
        """
        Deletes a note by its ID.
        """
        note_to_delete = None
        for note in self.notes:
            if note.id == note_id:
                note_to_delete = note
                break

        if note_to_delete:
            self.notes.remove(note_to_delete)
            print(f"{green}Note with ID {note_id} has been deleted.{reset}")
            self.save_to_file("notes.json")
        else:
            print(f"{red}No notes found with ID {note_id}.{reset}\n")

    def find_note_by_id(self, note_id):
        """
        Finds a note by its ID.
        """
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def save_to_file(self, file_name):
        """
        Saves the notebook to a JSON file.
        """
        with open(file_name, "w") as file:
            notes_dict = [note.to_dict() for note in self.notes]
            json.dump(notes_dict, file, indent=4)

    def load_from_file(self, file_name):
        """
        Loads notes from a JSON file into the notebook.
        """
        with open(file_name, "r") as file:
            notes_dict = json.load(file)
            self.notes = [Note.from_dict(note_data) for note_data in notes_dict]
