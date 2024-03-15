from src.error_handler import input_error
from src.classes import Record
import re

PHONE_MASK = r"^\d{10}$"
BLUE = "\033[94m"
ENDC = "\033[0m"


@input_error
def add_contact(args, address_book, is_consent=False):
    name, phone = args

    if not bool(re.fullmatch(PHONE_MASK, phone)):
        raise TypeError
    record = address_book.find(name)

    if record and not is_consent:
        return f"Here is a contact with name {name} yet. To overwrite? Type yes/no: "

    if not record:
        record = Record(name)

    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts):

    try:
        name, phone = args
    except:
        raise ValueError("The command is bad. Give me name and phone please.")

    if not bool(re.fullmatch(PHONE_MASK, phone)):
        raise TypeError

    record = contacts.find(name)

    if record:
        record.edit_phone(phone)
        return "Contact changed"
    else:
        return f"There isn't a contact with name {name}"


@input_error
def contact_phone(args, contacts):

    try:
        name = args[0]
    except IndexError:
        raise ValueError("The command is bad. Give me name")

    if name not in contacts:
        return f"There isn't a contacts with name {name}"

    return contacts[name]


@input_error
def all_contacts(contacts):
    if not contacts:
        return "No contacts to display."

    max_name_length = max(len(contact) for contact in contacts.keys())
    contact_list = ""

    for contact in contacts.values():
        phone = contact.phone if contact.phone else "No phone"
        birthday = (
            contact.birthday.value
            if contact.birthday and contact.birthday.value
            else "No information"
        )
        address = (
            contact.address.value
            if contact.address and contact.address.value
            else "No information"
        )
        email = (
            contact.email.value
            if contact.email and contact.email.value
            else "No information"
        )
        contact_list += f"{BLUE}{contact.name.value:<{max_name_length}}{ENDC}: phone: {phone}, birthday: {birthday}, address: {address}, email: {email}\n"
    return contact_list


@input_error
def add_birthday(args, address_book):
    name, birthday = args
    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        if record.birthday and record.birthday.value:
            return f"Birthday of {name}: {record.birthday.value}"
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
        return f"Address added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def change_address(args, contacts):

    try:
        name, old_addrees, new_address = args
    except:
        raise ValueError(
            "The command is bad. Give me name, old address and new address."
        )

    record = contacts.find(name)

    if record:
        record.edit_address(old_addrees, new_address)
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
        if record.address and record.address.value:
            return f"Address of {name}: {record.address.value}"
        else:
            return f"Address not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def delete_address(args, address_book):

    try:
        name, address = args
    except:
        raise ValueError("The command is bad. Give me name and address.")
    record = address_book.find(name)
    if record:
        record.remove_address(address)
        return f"Address {address} was deleted"
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
        return f"Email added for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def change_email(args, contacts):

    try:
        name, old_email, new_email = args
    except:
        raise ValueError("The command is bad. Give me name, old email and new email.")

    record = contacts.find(name)

    if record:
        record.edit_email(old_email, new_email)
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
        if record.email and record.email.value:
            return f"Email of {name}: {record.email.value}"
        else:
            return f"Email not set for {name}"
    else:
        return f"No contact found with name {name}"


@input_error
def delete_email(args, address_book):

    try:
        name, email = args
    except:
        raise ValueError("The command is bad. Give me name and email.")
    record = address_book.find(name)
    if record:
        record.remove_email(email)
        return f"Address {email} was deleted"
    else:
        return f"No contact found with name {name}"
