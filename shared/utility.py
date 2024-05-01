import re

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
username_regex = re.compile(r"^[a-zA-Z0-9._-]+$")


def check_email(email):
    if re.fullmatch(email_regex, email):
        return True


def check_username(username):
    if re.fullmatch(username_regex, username):
        return True
