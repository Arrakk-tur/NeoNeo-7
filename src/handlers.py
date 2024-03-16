from src.error_handler import input_error
from src.classes import Record, AddressBook
import re

BLUE = "\033[94m"
ENDC = "\033[0m"


@input_error
def add_contact(args, address_book, is_consent=False):
    name, phone = args

    record = address_book.find(name)

    if record and not is_consent:
        return f"Here is a contact with name {name} yet. To overwrite? Type yes/no: "

    if not record:
        record = Record(name)

    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."


@input_error
def change_phone(args, address_book):

    try:
        name, phone = args
    except:
        raise ValueError("The command is bad. Give me name and phone please.")

    # if not bool(re.fullmatch(PHONE_MASK, phone)):
    #     raise TypeError

    record = address_book.find(name)

    if record:
        record.edit_phone(phone)
        address_book.add_record(record)
        return "Contact changed"
    else:
        return f"There isn't a contact with name {name}"


@input_error
def show_phone(args, address_book):

    try:
        name = args[0]
    except:
        raise ValueError("The command is bad. Give me name")

    record = address_book.find(name)
    if record:
        if record.phone:
            return f"Phone of {name}: {record.phone}"
        else:
            return f"Phone not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def all_contacts(address_book):
    if not address_book:
        return "No contacts to display."
    else:
        [print(i[1]) for i in address_book.items()]


@input_error
def add_birthday(args, address_book):
    name, birthday = args
    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        address_book.add_record(record)
        return f"Birthday added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        if record.birthday:
            return f"Birthday of {name}: {record.birthday}"
        else:
            return f"Birthday not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def next_birthdays(args, address_book):
    if len(args) == 0:
        address_book.next_birthdays()
    else:
        days = args[0]
        address_book.next_birthdays(int(days))


@input_error
def add_address(args, address_book):
    try:
        name, address = args
    except:
        raise ValueError("The command is bad. Give me name and address.")

    record = address_book.find(name)
    if record:
        record.add_address(address)
        address_book.add_record(record)
        return f"Address added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def change_address(args, address_book):

    try:
        name, old_address, new_address = args
    except:
        raise ValueError(
            "The command is bad. Give me name, old address and new address."
        )

    record = address_book.find(name)

    if record:
        record.edit_address(old_address, new_address)
        address_book.add_record(record)
        return "Address changed"
    else:
        return f"There isn't a contact with name {name}"


@input_error
def show_address(args, address_book):
    try:
        name = args[0]
    except:
        raise ValueError("The command is bad. Give me name")

    record = address_book.find(name)
    if record:
        if record.address:
            return f"Address of {name}: {record.address}"
        else:
            return f"Address not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def delete_address(args, address_book):

    try:

        name = args[0]
    except:

        raise ValueError("The command is bad. Give me name.")
    record = address_book.find(name)
    if record:

        record.remove_address()
        address_book.add_record(record)

        return f"Address was deleted"
    else:
        return f"No contact found with name {name}"


@input_error
def add_email(args, address_book):
    try:
        name, email = args
    except:
        raise ValueError("The command is bad. Give me name and email.")

    record = address_book.find(name)
    if record:
        record.add_email(email)
        address_book.add_record(record)
        return f"Email added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def change_email(args, address_book):

    try:
        name, old_email, new_email = args
    except:
        raise ValueError("The command is bad. Give me name, old email and new email.")

    record = address_book.find(name)

    if record:
        record.edit_email(old_email, new_email)
        address_book.add_record(record)
        return "Email changed"
    else:
        return f"There isn't a contact with name {name}"


@input_error
def show_email(args, address_book):
    try:
        name = args[0]
    except:
        raise ValueError("The command is bad. Give me name")

    record = address_book.find(name)
    if record:
        if record.email:
            return f"Email of {name}: {record.email}"
        else:
            return f"Email not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def delete_email(args, address_book):

    try:

        name = args[0]
    except:

        raise ValueError("The command is bad. Give me name.")
    record = address_book.find(name)
    if record:

        record.remove_email()
        address_book.add_record(record)

        return f"Email was deleted"
    else:
        return f"No contact found with name {name}"
