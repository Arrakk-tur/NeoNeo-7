import json
from collections import UserDict, defaultdict
import re
from datetime import timedelta, datetime, date
import calendar


ADDRESS_BOOK_FILE_PATH = "address_book.json"


blue = "\033[94m"
reset = "\033[0m"
green = "\033[92m"
red = "\033[91m"
yellow = "\033[93m"


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
            raise ValueError(f"{red}Phone number must contain 10 digits.{reset}\n")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError(f"{red}The date format is not 'DD.MM.YYYY'{reset}\n")
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
                f"{red}Email must be in format (username)@(domainname).(top-leveldomain).{reset}\n"
            )
        super().__init__(value)


class Record:
    _last_id = 0

    def __init__(self, name, phone=None, birthday=None, address=None, email=None):
        Record._last_id += 1
        self.id = Record._last_id
        self.name = Name(name)
        self.phone = Phone(phone) if phone else None
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday and self.birthday.value:
            print(f"{green}Birthday: {self.birthday.value}.{reset}")
        else:
            print(f"{red}Birthday not set.{reset}\n")

    def remove_phone(self):
        self.phone = None

    def edit_phone(self, new_phone):
        self.phone = Phone(new_phone)

    def find_phone(self, phone):
        if self.phone and self.phone.value == phone:
            return self.phone
        return None

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, old_address, new_address):
        if self.address and self.address.value == old_address:
            self.address = Address(new_address)
        else:
            raise ValueError(
                f"{red}Contact doesn't have address {old_address}.{reset}\n"
            )

    def show_address(self):
        if self.address and self.address.value:
            print(f"{green}Address: {self.address.value}.{reset}")
        else:
            print(f"{red}Address not set.{reset}\n")

    def remove_address(self):
        self.address = None

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, old_email, new_email):
        if self.email and self.email.value == old_email:
            self.email = Email(new_email)
        else:
            raise ValueError(f"{red}Contact doesn't have email {old_email}.{reset}\n")

    def show_email(self):
        if self.email and self.email.value:
            print(f"{green}Email: {self.email.value}.{reset}")
        else:
            print(f"{red}Email not set.{reset}\n")

    def remove_email(self):
        self.email = None

    def record_to_dict(self):
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
    def add_record(self, record):
        self.data[record.id] = record
        self.save_contacts_to_file()

    def search(self, query):
        result = []
        query = query.lower()
        for record in self.data.values():
            if query in record.name.value.lower():
                result.append(str(record))
        return result if result else None

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record

    def delete_record(self, name):
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
                    upcoming_birthdays[next_birthday].append(record.name)
        if not upcoming_birthdays:
            print(f"{blue}No upcoming birthdays in the next {days} days.{reset}\n")
        else:
            print(f"{blue}Upcoming birthdays in the next {days} days:{reset}\n")
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
