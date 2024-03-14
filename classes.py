from collections import UserDict
import re
from datetime import date, timedelta, datetime


WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DELTA_MAP = {'Monday': 5, 'Sunday': 6}
BLUE = '\033[94m'
ENDC = '\033[0m'


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
        if value and not re.fullmatch(r"(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d{2}", value):
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = None
        self.birthday = Birthday(birthday) if birthday else None


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

    def __str__(self):
        return f"phone: {self.phone}"
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_birthdays_per_week(self):
        users = self.data.values()
        if not users:
            return([])

        this_week_birthdays = {}
        current_date = date.today()
        current_week_day = current_date.strftime("%A")
        delta = DELTA_MAP.get(current_week_day, 7)
        
        time_delta = timedelta(days=delta)
    
        for user in users:
            if user.birthday and user.birthday.value:
                birthday_date = datetime.strptime(user.birthday.value, '%d.%m.%Y')
                birthday_this_year = birthday_date.replace(year=current_date.year).date()
       
            
                if (birthday_this_year - current_date) > time_delta:
                    continue
            
                birthday_week_day = birthday_this_year.strftime('%A')
                
                if birthday_week_day in ('Saturday', 'Sunday'):
                    birthday_week_day = 'Monday'
                
                if birthday_week_day in this_week_birthdays:
                    this_week_birthdays[birthday_week_day].append(user.name.value)
                else:
                    this_week_birthdays[birthday_week_day] = [user.name.value]
            
        sorted_birthdays = {day: this_week_birthdays[day] for day in WEEK_DAYS if day in this_week_birthdays}
        
        for day, names in sorted_birthdays.items():
            print(f"{BLUE}{day:<9}{ENDC}: {', '.join(names)}")
        
        return

