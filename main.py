from src.classes import AddressBook
from src.handlers import *
from src.handler_notebook import *

blue, reset, green, red = "\033[94m", "\033[0m", "\033[92m", "\033[91m"


def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


def main():
    contacts = AddressBook()
    print(f"{blue}Welcome to the assistant bot!{reset}\n")

    try:
        notebook.load_from_file("notes.json")
        contacts.load_contacts_from_file()
    except FileNotFoundError:
        print(f"{blue}File not found. Starting with an empty DB.{reset}")

    while True:
        user_input = input(f"{blue}Enter a command: {reset}")
        command, *args = parse_input(user_input)

        if command in "close":
            print(f"{blue}Good bye!{reset}")
            exit()

        elif command == "help":
            help_command()

        elif command in [
            "add-contact",
            "change-phone",
            "show-phone",
            "add-birthday",
            "show-birthday",
            "next_birthdays",
            "add-address",
            "change-address",
            "show-address",
            "delete-address",
            "add-email",
            "change-email",
            "show-email",
            "delete-email",
            "search",
        ]:
            response = globals()[command.replace("-", "_")](args, contacts)
            print(response)

        elif command == "show-contacts":
            print(all_contacts(contacts))

        elif command == "delete":
            print(
                contacts.delete_record(" ".join(args))
                if args
                else "Please provide a name to delete."
            )

        elif command == "nadd":
            note_text = " ".join(args)
            if note_text:
                tags = [
                    tag.strip()
                    for tag in input(
                        f"{blue}Enter tags separated by commas (optional): {reset}"
                    ).split(",")
                    if tag.strip()
                ]
                add_note(note_text, tags)
                print(f"{green}Note was successfully created.{reset}")
            else:
                print(
                    f"{red}No text entered. Note was not created. Give me a text for note.{reset}\n"
                )

        elif command == "nfind":
            search_args = " ".join(args)
            tags = [arg for arg in search_args.split() if arg.startswith("#")]
            search_text = " ".join(
                arg for arg in search_args.split() if not arg.startswith("#")
            )
            find_notes(tags=tags, search_text=search_text)

        elif command == "nedit":
            if not args:
                print(f"{red}Enter note ID(a positive integer).{reset}\n")
                continue

            try:
                note_id = int(args[0])

                note = notebook.find_note_by_id(note_id)
                if note is None:
                    print(f"{red}There is no notates with id {note_id}.{reset}\n")
                    continue

            except:
                print(f"{red}Invalid input. Give me id(a positive integer).{reset}\n")
                continue

            new_text = input(f"{blue}Enter new text for the note: {reset}")
            tags = [
                tag.strip()
                for tag in input(
                    f"{blue}Enter tags separated by commas (optional): {reset}"
                ).split(",")
                if tag.strip()
            ]
            modify_note(note_id, new_text, tags)

        elif command == "ndel":
            if not args:
                print(
                    f"{red}No note ID provided. Please enter a note ID(a positive integer).{reset}\n"
                )
            else:
                delete_note(*args)

        elif command == "note":
            if not args:
                print(
                    f"{red}No note ID provided. Please enter a note ID(a positive integer).{reset}\n"
                )
            else:
                find_note_by_id(*args)

        elif not command:
            print(f"{red}No command.{reset}")

        else:
            print(f"{red}Invalid command.{reset}")


command_descriptions = {
    "close": "Close the program.",
    "add-contact": "Add a new contact.",
    "change-phone": "Change phone number for a contact.",
    "show-phone": "Show phone number for a contact.",
    "show-contacts": "Show all contacts.",
    "add-birthday": "Add birthday for a contact.",
    "show-birthday": "Show birthday for a contact.",
    "next_birthdays": "Show upcoming birthdays.",
    "add-address": "Add address for a contact.",
    "change-address": "Change address for a contact.",
    "show-address": "Show address for a contact.",
    "delete": "Delete a contact.",
    "delete-address": "Delete address for a contact.",
    "search": "Search contacts by name.",
    "add-email": "Add email for a contact.",
    "change-email": "Change email for a contact.",
    "show-email": "Show email for a contact.",
    "delete-email": "Delete email for a contact.",
    "nadd": "Add a new note.",
    "nfind": "Find notes by tag or text.",
    "nedit": "Edit an existing note.",
    "ndel": "Delete a note.",
    "note": "Find a note by ID.",
    "help": "Show available commands and their descriptions.",
}


def help_command():
    print("Available commands:")
    for command, description in command_descriptions.items():
        print(f"{(command + ':'):<15} {description}")


if __name__ == "__main__":
    main()
