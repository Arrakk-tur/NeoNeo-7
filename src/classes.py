import json
from collections import UserDict
import re
from datetime import date, timedelta, datetime

WEEK_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
DELTA_MAP = {"Monday": 5, "Sunday": 6}
ADDRESS_BOOK_FILE_PATH = "address_book.json"
BLUE = "\033[94m"
ENDC = "\033[0m"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value=None):
        if value and not re.fullmatch(
            r"(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d{2}", value
        ):
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    _last_id = 0

    def __init__(self, name, *args):
        Record._last_id += 1
        self.id = Record._last_id
        self.name = Name(name)
        self.phone = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        self.phone = phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

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
        self.address = Address(address)

    def edit_address(self, old_address, new_adress):

        if self.address.value == old_address:
            self.address = Address(new_adress)
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

    def __str__(self):
        return f"phone: {self.phone}"

    def record_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "birthday": self.birthday,
            # "email": self.email,
            "address": self.address,
        }

    @staticmethod
    def record_from_dict(data):
        record = Record(
            data["name"], data["phone"], data["birthday"]
        )  # , data["email"], data["address"])
        record.id = data["id"]

        return record


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        self.save_contacts_to_file()

    def find(self, name):
        return self.data.get(name)

    # TODO: Realize this deleting by id
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # TODO: Rewrite this function to seve data in json
    def save_contacts_to_file(self):
        with open(ADDRESS_BOOK_FILE_PATH, "w") as file:
            address_book_dict = [rec for rec in self.data.items()]
            json.dump(address_book_dict, file, indent=4)

    def load_contacts_from_file(self):
        with open(ADDRESS_BOOK_FILE_PATH, "r") as file:
            upload_data = json.load(file)
            for i in upload_data:
                self.data[i] = Record.record_from_dict(upload_data[i])

    def get_birthdays_per_week(self):
        users = self.data.values()
        if not users:
            return []

        this_week_birthdays = {}
        current_date = date.today()
        current_week_day = current_date.strftime("%A")
        delta = DELTA_MAP.get(current_week_day, 7)

        time_delta = timedelta(days=delta)

        for user in users:
            if user.birthday and user.birthday.value:
                birthday_date = datetime.strptime(user.birthday.value, "%d.%m.%Y")
                birthday_this_year = birthday_date.replace(
                    year=current_date.year
                ).date()

                if (birthday_this_year - current_date) > time_delta:
                    continue

                birthday_week_day = birthday_this_year.strftime("%A")

                if birthday_week_day in ("Saturday", "Sunday"):
                    birthday_week_day = "Monday"

                if birthday_week_day in this_week_birthdays:
                    this_week_birthdays[birthday_week_day].append(user.name.value)
                else:
                    this_week_birthdays[birthday_week_day] = [user.name.value]

        sorted_birthdays = {
            day: this_week_birthdays[day]
            for day in WEEK_DAYS
            if day in this_week_birthdays
        }

        for day, names in sorted_birthdays.items():
            print(f"{BLUE}{day:<9}{ENDC}: {', '.join(names)}")

        return
