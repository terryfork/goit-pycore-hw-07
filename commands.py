from addressbook import AddressBook, Record

done = False

book = AddressBook()


def input_error(func):
    def inner(params):
        command = func.__name__.removesuffix('_handler')
        command_params = []
        helper_name = command+"_helper"
        if helper_name in globals().keys():
            command_helper = globals()[helper_name]
            command_params = command_helper()
            if len(params) != len(command_params):
                return f"Usage: {command} <" + "> <".join(command_params) + ">"
        else:
            if len(params) > 0:
                return f"Usage: {command}"
        try:
            return func(params)
        except Exception as e:
            return f"Error occurred: {e}"
    return inner


@input_error
def hello_handler(params):
    return "Hello, my dear! Have a nice day!"


@input_error
def add_handler(params):
    rec = Record(params[0], params[1])
    return book.add_record(rec)


def add_helper():
    return ['name', 'phone']


@input_error
def add_birthday_handler(params):
    rec = book.find(params[0])
    if rec:
        return rec.add_birthday(params[1])
    else:
        return "Contact not found"


def add_birthday_helper():
    return ['name', 'dob']


@input_error
def change_handler(params):
    rec = book.find(params[0])
    if rec:
        return rec.edit_phone(params[1], params[2])
    else:
        return "Contact not found"


def change_helper():
    return ['name', 'old_phone', 'new_phone']


@input_error
def phone_handler(params):
    return book.get_phones(params[0])


def phone_helper():
    return ['name']


@input_error
def all_handler(params):
    return book.get_all()


@input_error
def exit_handler(params):
    global done
    done = True
    return "Bye!"


def close_handler(params):
    return exit_handler(params)


def get_upcoming_birthdays_handler(params):
    return book.get_upcoming_birthdays(int(params[0]))


def get_upcoming_birthdays_helper():
    return ['days']


@input_error
def help_handler(params):
    all_commands = [
        func.replace("_handler", "")
        for func in globals().keys() if func.endswith("_handler")
    ]
    return "Available comands: " + " ".join(all_commands)
