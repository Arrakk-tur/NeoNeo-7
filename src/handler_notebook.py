from src.class_notebook import Notebook
from src.error_handler import input_error
from datetime import datetime

blue = "\033[94m"
reset = "\033[0m"
green = "\033[92m"
red = "\033[91m"

notebook = Notebook()


@input_error
def add_note(text, tags=None):
    notebook.add_note(text, tags)


@input_error
def find_notes(tags=[], search_text=""):
    found_notes = notebook.notes

    if len(tags):
        cleaned_tags = [tag.replace("#", "") for tag in tags]
        found_notes = notebook.find_notes(cleaned_tags) if tags else notebook.notes

    if search_text:
        found_notes = [note for note in found_notes if search_text in note.text]

    if not len(found_notes):
        print(f"{red}No notes were found matching the search query.{red}\n")
        return

    print(f"\n{green}Your search yielded {len(found_notes)} notes:{reset}\n")

    for note in found_notes:
        print_note(note)


@input_error
def modify_note(note_id, new_text="", new_tags=None):
    if new_text:
        notebook.modify_note(note_id, new_text)

    if len(new_tags):
        notebook.modify_tags(note_id, new_tags)

    if not new_text and not len(new_tags):
        print(
            f"{red}The note was not modified as no replacement data was provided. Give me a new text for note {reset}\n"
        )
    else:
        print(f"{green}The note has been successfully updated.{reset}\n")


@input_error
def delete_note(note_id):
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
    try:
        note_id = int(note_id)
        note = notebook.find_note_by_id(note_id)
        if not note:
            print(f"{green}No notes were found with id {note_id}{reset}\n")

        print_note(note)
    except ValueError:
        print(f"{red}Invalid note ID: {note_id}. Note ID must be an integer.{reset}\n")
    except IndexError:
        print(f"{red}No note found with ID {note_id}.{reset}\n")


def print_note(note):
    tags_str = ", ".join(note.tags)
    formatted_date = note.creation_date.strftime("%Y-%m-%d")

    note_for_print = f"\n{green}Note:\n{blue}id{reset}: {note.id}, {blue}date{reset}: {formatted_date}\n{blue}tags{reset}: {tags_str}\n{note.text}\n"
    print(note_for_print)
