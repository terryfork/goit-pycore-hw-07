from collections import UserDict
from datetime import datetime, date, timedelta
from calendar import isleap
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validator(self, val):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.validator(val):
            self._value = val
        else:
            raise ValueError(
                f"Invalid value for field {self.__class__.__name__}: {val}"
            )


class Name(Field):
    def validator(self, name):
        return type(name) is str and len(name) > 0


class Phone(Field):
    def validator(self, phone_str):
        return re.match(r"^\d{10}+$", phone_str) is not None


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def validator(self, dob):
        try:
            if datetime.strptime(dob, self.DATE_FORMAT):
                return True
        except ValueError:
            return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.validator(value):
            self._value = datetime.strptime(value, self.DATE_FORMAT).date()
        else:
            raise ValueError(
                f"Invalid value for field {self.__class__.__name__}: {value}"
            )

    def get_greet_date(self, year):
        if (
            self.value.month == 2 and
            self.value.day == 29 and
            not isleap(year)
        ):
            bd = date(year=year, month=2, day=28)
        else:
            bd = date(year=year, month=self.value.month, day=self.value.day)
        weekday = bd.weekday()
        greet_date = bd + timedelta(days=7-weekday) if weekday > 4 else bd
        return greet_date

    def __str__(self):
        return self.value.strftime(self.DATE_FORMAT)


class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.add_phone(phone)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj.value not in [p.value for p in self.phones]:
            self.phones.append(phone_obj)
            return "Phone added"
        return "Phone already exists"

    def add_birthday(self, dob):
        self.birthday = Birthday(dob)
        return "Birthday added"

    def edit_phone(self, phone_old, phone_new):
        for phone_obj in self.phones:
            if phone_obj.value == phone_old:
                phone_obj.value = phone_new
                return "Phone changed"
        return "Phone not found"

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

    def remove_phone(self, phone):
        for idx, phone_obj in enumerate(self.phones):
            if phone_obj.value == phone:
                del self.phones[idx]

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, phones: "
            f"{'; '.join(p.value for p in self.phones)} "
            f"birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, rec):
        if rec.name.value not in self.data:
            self.data[rec.name.value] = rec
            return "Contact added"
        else:
            rec_exist = self.data[rec.name.value]
            return "Contact exist. " + rec_exist.add_phone(rec.phones[0].value)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_phones(self, name):
        if name in self.data:
            phones = self.data[name].phones
            return ", ".join(p.value for p in phones)
        else:
            return "Contact not found"

    def get_all(self):
        return "\n".join(str(rec) for rec in self.data.values())

    def get_upcoming_birthdays(self, days):
        today = date.today()
        upcom_bds = {}
        for name, rec in self.data.items():
            if rec.birthday:
                greet_date = rec.birthday.get_greet_date(today.year)
                if greet_date < today:
                    greet_date = rec.birthday.get_greet_date(today.year+1)
                delta = greet_date - today
                if delta.days <= days:
                    upcom_bds[rec.name.value] = greet_date.strftime(Birthday.DATE_FORMAT)
        return "\n".join(f"{name} - greeting date: {greet}" for name, greet in upcom_bds.items())
