import re


def emailVal(email):
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

    if re.match(pattern, email) is not None:
        return True
    else:
        return False


def numberVal(number):
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'

    if re.match(pattern, number) is not None:
        return True
    else:
        return False
