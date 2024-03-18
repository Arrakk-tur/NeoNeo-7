from src.error_handler import input_error
from src.classes import Record, AddressBook
import re


blue = "\033[94m"
reset = "\033[0m"
green = "\033[92m"
red = "\033[91m"


@input_error
def add_contact(args, address_book, is_consent=False):

    try:
        name, phone = args

    except:
        raise ValueError(
            f"{red}The command is bad. Give me name and phone please.{reset}\n"
        )

        # record = address_book.find(name)

        # if record and not is_consent:
        #     return f"Here is a contact with name {name} yet. To overwrite? Type yes/no: "

        # if not record:
    record = Record(name)

    record.add_phone(phone)
    address_book.add_record(record)
    return f"{green}Contact added.{reset}"


@input_error
def change_phone(args, address_book):

    try:
        name, phone = args
    except:
        raise ValueError(
            f"{red}The command is bad. Give me name and phone please.{reset}\n"
        )

    # if not bool(re.fullmatch(PHONE_MASK, phone)):
    #     raise TypeError

    record = address_book.find(name)

    if record:
        record.edit_phone(phone)
        address_book.add_record(record)
        return f"{green}Contact changed.{reset}"
    else:
        return f"{red}There isn't a contact with name {name}.{reset}\n"


@input_error
def show_phone(args, address_book):

    try:
        name = args[0]
    except:
        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")

    record = address_book.find(name)
    if record:
        if record.phone:
            return f"{green}Phone of {name}: {record.phone}.{reset}"
        else:
            return f"{red}Phone not set for {name}.{reset}\n"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def all_contacts(address_book):
    if not address_book:
        return "No contacts to display."
    else:
        header()
        contacts = []
        for record in address_book.values():
            contacts.append(str(record))

        return "\n".join(contacts)


@input_error
def add_birthday(args, address_book):
    try:
        name, birthday = args
    except:
        raise ValueError(
            f"{red}The command is bad. Give me name and birthday in format DD.MM.YYYY.{reset}\n "
        )

    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        address_book.add_record(record)
        return f"{green}Birthday added for {name}.{reset}"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def show_birthday(args, address_book):
    try:
        name = args[0]
    except:
        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")

    record = address_book.find(name)
    if record:
        if record.birthday:
            return f"{green}Birthday of {name}: {record.birthday}.{reset}"
        else:
            return f"{red}Birthday not set for {name}.{reset}\n"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def next_birthdays(args, address_book):
    if len(args) == 0:
        return address_book.next_birthdays()
    else:
        days = args[0]
        try:
            return address_book.next_birthdays(int(days))
        except:
            raise ValueError(
                f"{red}The command is bad. Give me an positive integer.{reset}\n"
            )


@input_error
def add_address(args, address_book):
    try:
        name, address = args
    except:
        raise ValueError(f"{red}The command is bad. Give me name and address.{reset}\n")

    record = address_book.find(name)
    if record:
        record.add_address(address)
        address_book.add_record(record)
        return f"{green}Address added for {name}.{reset}"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def change_address(args, address_book):

    try:
        name, old_address, new_address = args
    except:
        raise ValueError(
            f"{red}The command is bad. Give me name, old address and new address.{reset}\n"
        )

    record = address_book.find(name)

    if record:
        record.edit_address(old_address, new_address)
        address_book.add_record(record)
        return f"{green}Address changed.{reset}"
    else:
        return f"{red}There isn't a contact with name {name}.{reset}\n"


@input_error
def show_address(args, address_book):
    try:
        name = args[0]
    except:
        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")

    record = address_book.find(name)
    if record:
        if record.address:
            return f"{green}Address of {name}: {record.address}.{reset}"
        else:
            return f"{red}Address not set for {name}.{reset}\n"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def delete_address(args, address_book):

    try:

        name = args[0]
    except:

        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")
    record = address_book.find(name)
    if record:

        record.remove_address()
        address_book.add_record(record)

        return f"{green}Address was deleted{reset}"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def add_email(args, address_book):
    try:
        name, email = args
    except:
        raise ValueError(f"{red}The command is bad. Give me name and email.{reset}\n")

    record = address_book.find(name)
    if record:
        record.add_email(email)
        address_book.add_record(record)
        return f"{green}Email added for {name}.{reset}"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def change_email(args, address_book):

    try:
        name, old_email, new_email = args
    except:
        raise ValueError(
            f"{red}The command is bad. Give me name, old email and new email.{reset}\n"
        )

    record = address_book.find(name)

    if record:
        record.edit_email(old_email, new_email)
        address_book.add_record(record)
        return f"{green}Email changed.{reset}"
    else:
        return f"{red}There isn't a contact with name {name}.{reset}\n"


@input_error
def show_email(args, address_book):
    try:
        name = args[0]
    except:
        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")

    record = address_book.find(name)
    if record:
        if record.email:
            return f"{green}Email of {name}: {record.email}.{reset}"
        else:
            return f"{red}Email not set for {name}.{reset}\n"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def delete_email(args, address_book):

    try:

        name = args[0]
    except:

        raise ValueError(f"{red}The command is bad. Give me name.{reset}\n")
    record = address_book.find(name)
    if record:

        record.remove_email()
        address_book.add_record(record)

        return f"{green}Email was deleted.{reset}"
    else:
        return f"{red}No contact found with name {name}.{reset}\n"


@input_error
def search(args, address_book):
    found_records = address_book.search(" ".join(args))
    if found_records is None:
        return f"{red}No contacts found matching your search.{reset}\n"
    else:
        header()
        return "\n".join(found_records)


def header():
    print(f"{'-' * 124}")
    print(
        f"| {'Name':^20} | {'Phone':^20} | {'Email':^20} | {'Birthday':^20} | {'Address':^20} | {'ID':^5} |"
    )
    print(f"|{(('-' * 22) + '+') * 5}-------|")
