import json
from collections import UserDict, defaultdict
import re
from datetime import timedelta, datetime, date
import calendar


ADDRESS_BOOK_FILE_PATH = "address_book.json"

blue, reset, green, red, yellow = "\033[94m", "\033[0m", "\033[92m", "\033[91m", "\033[93m"


class Field:
    """
    Base class for representing a generic field.

    Attributes:
        value: The value associated with the field.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Represents a person's name.

    Args:
        value (str): The name value.
    """
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """
   Represents a phone number.

   Args:
       value (str): The phone number value (must contain 10 digits).
   """
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError(f"{red}Phone number must contain 10 digits.{reset}\n")
        super().__init__(value)


class Birthday(Field):
    """
    Represents a person's birthday.

    Args:
        birthday (str): The birthday value in 'DD.MM.YYYY' format.
    """
    def __init__(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError(f"{red}The date format is not 'DD.MM.YYYY'{reset}\n")
        super().__init__(birthday)


class Address(Field):
    """
    Represents a physical address.

    Args:
        value (str): The address value.
    """
    def __init__(self, value):
        super().__init__(value)


class Email(Field):
    """
    Represents an email address.

    Args:
        value (str): The email address value (must be in format 'username@domain.top-leveldomain').
    """
    def __init__(self, value):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if not re.fullmatch(regex, value):
            raise ValueError(
                f"{red}Email must be in format (username)@(domainname).(top-leveldomain).{reset}\n"
            )
        super().__init__(value)


class Record:
    """
    Represents a contact record with associated information such as name, phone number, birthday, address, and email.

    Attributes:
        id (int): Unique identifier for the record.
        name (Name): Name object representing the contact's name.
        phone (Phone): Phone object representing the contact's phone number.
        email (Email): Email object representing the contact's email address.
        birthday (Birthday): Birthday object representing the contact's birthday.
        address (Address): Address object representing the contact's address.

    Methods:
        __init__: Initializes a Record object with provided attributes.
        add_phone: Adds a phone number to the record.
        remove_phone: Removes the phone number from the record.
        edit_phone: Modifies the phone number of the contact.
        find_phone: Searches for a phone number within the record.
        add_birthday: Adds a birthday to the record.
        show_birthday: Displays the birthday of the contact.
        add_address: Adds an address to the record.
        edit_address: Modifies the address of the contact.
        show_address: Displays the address of the contact.
        remove_address: Removes the address from the record.
        add_email: Adds an email address to the record.
        edit_email: Modifies the email address of the contact.
        show_email: Displays the email address of the contact.
        remove_email: Removes the email address from the record.
        record_to_dict: Converts the record to a dictionary.
        record_from_dict: Creates a Record object from a dictionary.

    """

    _last_id = 0

    def __init__(self, name, phone=None, birthday=None, address=None, email=None):
        """
        Initializes a Record object with provided attributes.

        Args:
            name (str): Name of the contact.
            phone (str, optional): Phone number of the contact.
            birthday (str, optional): Birthday of the contact.
            address (str, optional): Address of the contact.
            email (str, optional): Email address of the contact.
        """
        Record._last_id += 1
        self.id = Record._last_id
        self.name = Name(name)
        self.phone = Phone(phone) if phone else None
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None

# Phone block
    def add_phone(self, phone):
        """
        Adds a phone number to the record.

        Args:
            phone (str): Phone number to add to the record.
        """
        self.phone = Phone(phone)

    def remove_phone(self):
        """
        Removes the phone number from the record.
        """
        self.phone = None

    def edit_phone(self, new_phone):
        """
        Modifies the phone number of the contact.

        Args:
            new_phone (str): New phone number for the contact.
        """
        self.phone = Phone(new_phone)

    def find_phone(self, phone):
        """
          Searches for a phone number within the record.

          Args:
              phone (str): Phone number to search for.

          Returns:
              Phone: Phone object if found, None otherwise.
          """
        if self.phone and self.phone.value == phone:
            return self.phone
        return None

# Birthday block
    def add_birthday(self, birthday):
        """
        Adds a birthday to the record.

        Args:
            birthday (str): Birthday to add to the record.
        """
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        """
        Displays the birthday of the contact if available.
        """
        if self.birthday and self.birthday.value:
            print(f"{green}Birthday: {self.birthday.value}.{reset}")
        else:
            print(f"{red}Birthday not set.{reset}\n")

# Address block
    def add_address(self, address):
        """
        Adds an address to the record.

        Args:
            address (str): Address to add to the record.
        """
        self.address = Address(address)

    def edit_address(self, old_address, new_address):
        """
        Modifies the address of the contact.

        Args:
            old_address (str): Old address of the contact.
            new_address (str): New address for the contact.

        Raises:
            ValueError: If the contact does not have the provided old address.
        """
        if self.address and self.address.value == old_address:
            self.address = Address(new_address)
        else:
            raise ValueError(
                f"{red}Contact doesn't have address {old_address}.{reset}\n"
            )

    def show_address(self):
        """
        Displays the address of the contact if available.
        """
        if self.address and self.address.value:
            print(f"{green}Address: {self.address.value}.{reset}")
        else:
            print(f"{red}Address not set.{reset}\n")

    def remove_address(self):
        """
        Removes the address from the record.
        """
        self.address = None

# Email block
    def add_email(self, email):
        """
        Adds an email address to the record.

        Args:
            email (str): Email address to add to the record.
        """
        self.email = Email(email)

    def edit_email(self, old_email, new_email):
        """
        Modifies the email address of the contact.

        Args:
            old_email (str): Old email address of the contact.
            new_email (str): New email address for the contact.

        Raises:
            ValueError: If the contact does not have the provided old email address.
        """
        if self.email and self.email.value == old_email:
            self.email = Email(new_email)
        else:
            raise ValueError(f"{red}Contact doesn't have email {old_email}.{reset}\n")

    def show_email(self):
        """
        Displays the email address of the contact if available.
        """
        if self.email and self.email.value:
            print(f"{green}Email: {self.email.value}.{reset}")
        else:
            print(f"{red}Email not set.{reset}\n")

    def remove_email(self):
        """
        Removes the email address from the record.
        """
        self.email = None

# Dictionary methods

    def record_to_dict(self):
        """
        Converts the record to a dictionary.

        Returns:
            dict: Dictionary representation of the record.
        """
        return {
            "id": self.id,
            "name": self.name.value,
            "phone": self.phone.value if self.phone else None,
            "birthday": self.birthday.value if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def record_from_dict(cls, data):
        """
        Creates a Record object from a dictionary.

        Args:
            data (dict): Dictionary containing record data.

        Returns:
            Record: Record object created from the provided dictionary.
        """
        return cls(
            name=data.get("name"),
            phone=data.get("phone"),
            birthday=data.get("birthday"),
            email=data.get("email"),
            address=data.get("address"),
        )

    def __str__(self):
        address = f"{self.address.value if self.address else '':^20}"
        birthday = f"{self.birthday.value if self.birthday else '':^20}"
        email = f"{self.email.value if self.email else '':^20}"
        phone = f"{self.phone.value:^20}"
        separator = f"|{(('-'*22)+'+')*5}-------|"
        contact_info = f"| {yellow}{self.name.value:<20}{reset} | {phone} | {email} | {birthday} | {address} | {self.id:^5} |"
        return f"{contact_info}\n{separator}"


class AddressBook(UserDict):
    """
    Represents an address book to manage contacts.

    Methods:
        add_record: Adds a record to the address book.
        search: Searches for records containing a given query in the name.
        find: Finds a record by name.
        delete_record: Deletes a record by name.
        save_contacts_to_file: Saves contacts to a file in JSON format.
        load_contacts_from_file: Loads contacts from a JSON file.
        next_birthdays: Finds upcoming birthdays within a specified number of days.

    """

    def add_record(self, record):
        """
        Adds a record to the address book.

        Args:
            record (Record): Record object to add to the address book.
        """
        self.data[record.id] = record
        self.save_contacts_to_file()

    def search(self, query):
        """
        Searches for records containing a given query in the name.

        Args:
            query (str): Query string to search for in the names.

        Returns:
            list: List of records matching the query.
        """
        result = []
        query = query.lower()
        for record in self.data.values():
            if query in record.name.value.lower():
                result.append(str(record))
        return result if result else None

    def find(self, name):
        """
       Finds a record by name.

       Args:
           name (str): Name of the contact to find.

       Returns:
           Record: Record object if found, None otherwise.
       """
        for record in self.data.values():
            if record.name.value == name:
                return record

    def delete_record(self, name):
        """
        Deletes a record by name.

        Args:
            name (str): Name of the contact to delete.

        Returns:
            str: Confirmation message indicating success or failure of deletion.
        """
        to_delete_id = None
        for record_id, record in self.data.items():
            if record.name.value.lower() == name.lower():
                to_delete_id = record_id
                break
        if to_delete_id:
            del self.data[to_delete_id]
            self.save_contacts_to_file()
            return (
                f"{green}Contact with the name {name} was successfully deleted.{reset}"
            )
        else:
            return f"{red}Contact with the name {name} was not found.{reset}\n"

    def save_contacts_to_file(self):
        """
        Saves contacts to a file in JSON format.
        """
        with open(ADDRESS_BOOK_FILE_PATH, "w") as file:
            address_book_dict = [rec[1].record_to_dict() for rec in self.data.items()]
            json.dump(address_book_dict, file, indent=4)

    def load_contacts_from_file(self):
        """
        Loads contacts from a JSON file.
        """
        with open(ADDRESS_BOOK_FILE_PATH, "r") as file:
            upload_data = json.load(file)
            for data in upload_data:
                record = Record.record_from_dict(data)
                self.add_record(record)

    # Birthday methods
    def next_birthdays(self, days=7):
        """
        Finds upcoming birthdays within a specified number of days.

        Args:
            days (int): Number of days to look ahead for upcoming birthdays. Default is 7.

        Returns:
            str: String representation of upcoming birthdays within the specified days.
        """
        WEEKDAYS = list(calendar.day_name)
        CURRENT_DATE = datetime.today().date()
        upcoming_birthdays = defaultdict(list)
        for name, record in self.data.items():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                next_birthday = datetime(CURRENT_DATE.year, bday.month, bday.day).date()
                if CURRENT_DATE <= next_birthday <= CURRENT_DATE + timedelta(days=days):
                    upcoming_birthdays[next_birthday].append(record.name)
        if not upcoming_birthdays:
            print(f"{blue}No upcoming birthdays in the next {days} days.{reset}")
        else:
            print(f"{blue}Upcoming birthdays in the next {days} days:{reset}")
            des = []
            for next_birthday, names in sorted(upcoming_birthdays.items()):
                day_of_week = WEEKDAYS[next_birthday.weekday()]
                formatted_names = ", ".join(
                    [
                        f"{yellow}{name}{reset} ({next_birthday.strftime('%d.%m.%Y')})"
                        for name in names
                    ]
                )
                des.append(f"\n{day_of_week:10}: {formatted_names}")
            return "".join(des)
