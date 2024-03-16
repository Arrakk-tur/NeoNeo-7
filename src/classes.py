import json
from collections import UserDict, defaultdict
import re
from datetime import timedelta, datetime, date
import calendar


ADDRESS_BOOK_FILE_PATH = "address_book.json"
BLUE = "\033[94m"
ENDC = "\033[0m"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError("The date format is not 'DD.MM.YYYY'")
        super().__init__(birthday)


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if not re.fullmatch(regex, value):
            raise ValueError(
                "Email must be in format (username)@(domainname).(top-leveldomain)"
            )
        super().__init__(value)


class Record:
    _last_id = 0

    def __init__(self, name, phone=None, birthday=None, address=None, email=None):
        Record._last_id += 1
        self.id = Record._last_id
        self.name = name
        self.phone = phone
        self.email = email
        # self.birthday = Birthday(birthday) if birthday else None
        self.birthday = birthday
        self.address = address

    def add_phone(self, phone):
        self.phone = phone

    def add_birthday(self, birthday):
        self.birthday = birthday

    def show_birthday(self):
        if self.birthday and self.birthday.value:
            print(f"Birthday: {self.birthday.value}")
        else:
            print("Birthday not set")

    def remove_phone(self, phone):
        self.phone = None

    def edit_phone(self, new_phone):
        self.phone = new_phone

    def find_phone(self, phone):
        for p in self.phone:
            if p.value == phone:
                return p
        return None

    def add_address(self, address):
        # self.address = Address(address)
        self.address = address

    def edit_address(self, old_address, new_address):

        if self.address.value == old_address:
            self.address = Address(new_address)
        else:
            raise ValueError(f"Contact don't have address {old_address}")

    def show_address(self):
        if self.address and self.address.value:
            print(f"Address: {self.address.value}")
        else:
            print("Address not set")

    def remove_address(self, address):
        if self.address.value == address:
            self.address = None
        else:
            raise ValueError(f"Adress {address} doesn't exist")

    def add_email(self, email):
        self.email = email

    def edit_email(self, old_email, new_email):

        if self.email.value == old_email:
            self.email = Email(new_email)
        else:
            raise ValueError(f"Contact don't have email {old_email}")

    def show_email(self):
        if self.email and self.email.value:
            print(f"Email: {self.email.value}")
        else:
            print("Email not set")

    def remove_email(self, email):
        if self.email.value == email:
            self.email = None
        else:
            raise ValueError(f"Email {email} doesn't exist")

    def record_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "birthday": self.birthday,
            "email": self.email,
            "address": self.address,
        }

    @classmethod
    def record_from_dict(cls, data):
        return cls(
            name=data.get("name"),
            phone=data.get("phone"),
            birthday=data.get("birthday"),
            email=data.get("email"),
            address=data.get("address"),
        )

    def __str__(self):
        birthday = "" if self.birthday is None else f", birthday: {self.birthday}"
        address = "" if self.address is None else f", address: {self.address}"
        email = "" if self.email is None else f", email: {self.email}"
        return f"{BLUE}{self.name}{ENDC}: phone: {self.phone}{birthday}{address}{email}, id: {self.id}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.id] = record
        self.save_contacts_to_file()

    def search(self, query):
        result = []
        query = query.lower()
        for name, record in self.data.items():
            if query in name.lower():
                result.append(record)
        return result

    def find(self, name):
        for record in self.data.values():
            if record.name == name:
                return record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} has been successfully deleted."
        else:
            return f"Record with name {name} not found."

    def save_contacts_to_file(self):
        with open(ADDRESS_BOOK_FILE_PATH, "w") as file:
            address_book_dict = [rec[1].record_to_dict() for rec in self.data.items()]
            json.dump(address_book_dict, file, indent=4)

    def load_contacts_from_file(self):
        with open(ADDRESS_BOOK_FILE_PATH, "r") as file:
            upload_data = json.load(file)
            for data in upload_data:
                record = Record.record_from_dict(data)
                self.add_record(record)

    # Birthday methods
    def next_birthdays(self, days=7):
        WEEKDAYS = list(calendar.day_name)
        CURRENT_DATE = datetime.today().date()
        upcoming_birthdays = defaultdict(list)
        for name, record in self.data.items():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                next_birthday = datetime(CURRENT_DATE.year, bday.month, bday.day).date()
                if CURRENT_DATE <= next_birthday <= CURRENT_DATE + timedelta(days=days):
                    upcoming_birthdays[next_birthday].append(name)
        if not upcoming_birthdays:
            print(f"No upcoming birthdays in the next {days} days.")
        else:
            desc = f"Upcoming birthdays in the next {days} days:"
            for next_birthday, names in sorted(upcoming_birthdays.items()):
                day_of_week = WEEKDAYS[next_birthday.weekday()]
                formatted_names = ", ".join(
                    [f"{name} ({next_birthday.strftime('%d.%m.%Y')})" for name in names]
                )
                desc += f"\n{day_of_week}: {formatted_names}"
            print(desc)
