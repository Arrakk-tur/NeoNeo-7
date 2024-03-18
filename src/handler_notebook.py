from src.class_notebook import Notebook
from src.error_handler import input_error
from datetime import datetime

blue, reset, green, red, yellow = "\033[94m", "\033[0m", "\033[92m", "\033[91m", "\033[93m"


notebook = Notebook()


@input_error
def add_note(text, tags=None):
    """
    Adds a new note to the notebook.

    Args:
        text (str): The content of the note.
        tags (list, optional): List of tags associated with the note. Defaults to None.
    """
    notebook.add_note(text, tags)


@input_error
def find_notes(tags=[], search_text=""):
    """
    Finds notes based on tags and/or text content.

    Args:
        tags (list, optional): List of tags to search for. Defaults to [].
        search_text (str, optional): Text to search for within notes. Defaults to "".
    """
    found_notes = notebook.notes

    if len(tags):
        cleaned_tags = [tag.replace("#", "") for tag in tags]
        found_notes = notebook.find_notes(cleaned_tags) if tags else notebook.notes

    if search_text:
        found_notes = [note for note in found_notes if search_text in note.text]

    if not len(found_notes):
        print(f"{red}No notes were found matching the search query.{reset}\n")
        return

    print(f"\n{green}Your search yielded {len(found_notes)} notes:{reset}\n")

    for note in found_notes:
        print_note(note)


@input_error
def modify_note(note_id, new_text="", new_tags=None):
    """
    Modifies the text content and/or tags of a note.

    Args:
        note_id (int): The ID of the note to modify.
        new_text (str, optional): The new content of the note. Defaults to "".
        new_tags (list, optional): List of new tags for the note. Defaults to None.
    """
    if new_text:
        notebook.modify_note(note_id, new_text)

    if len(new_tags):
        notebook.modify_tags(note_id, new_tags)

    if not new_text and not len(new_tags):
        print(
            f"{red}The note was not modified as no replacement data was provided. Give me a new text for note {reset}\n"
        )
    else:
        print(f"{green}The note has been successfully updated.{reset}")


@input_error
def delete_note(note_id):
    """
    Deletes a note by its ID.

    Args:
        note_id (int): The ID of the note to delete.
    """
    if not note_id:
        print(f"{red}No note ID provided. Please enter a note ID.{reset}\n")
        return

    try:
        note_id = int(note_id)
        notebook.delete_note(note_id)
    except ValueError:
        print(f"{red}Invalid note ID: {note_id}. Note ID must be an integer.{reset}\n")


@input_error
def find_note_by_id(note_id):
    """
    Finds a note by its ID and prints it.

    Args:
        note_id (int): The ID of the note to find.
    """
    try:
        note_id = int(note_id)
        note = notebook.find_note_by_id(note_id)
        if not note:
            print(f"{red}No notes were found with id {note_id}{reset}\n")

        print_note(note)
    except ValueError:
        print(f"{red}Invalid note ID: {note_id}. Note ID must be an integer.{reset}\n")
    except IndexError:
        print(f"{red}No notes were found with ID {note_id}.{reset}\n")


def print_note(note):
    """
    Prints the details of a given note.

    Args:
        note (Note): The note to print.
    """
    tags_str = ", ".join(note.tags)
    formatted_date = note.creation_date.strftime("%Y-%m-%d")

    note_for_print = f"\n{green}Note:\n{blue}id{reset}: {note.id}, {blue}date{reset}: {formatted_date}\n{blue}tags{reset}: {tags_str}\n{note.text}\n"
    print(note_for_print)
