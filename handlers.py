from error_handler import input_error
from classes import Record
import re

PHONE_MASK = r"^\d{10}$"
BLUE = '\033[94m'
ENDC = '\033[0m'


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
        return 'Contact changed'
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
    contact_list = ''
    
    for contact in contacts.values():
        phone = contact.phone if contact.phone else "No phone"
        birthday = contact.birthday.value if contact.birthday and contact.birthday.value else "No information"
        contact_list += f"{BLUE}{contact.name.value:<{max_name_length}}{ENDC}: phone: {phone}, birthday: {birthday}\n"
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
def birthdays(address_book):
    address_book.get_birthdays_per_week()
