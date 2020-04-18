from tools.mysql import *

from datetime import datetime
from getpass import getpass
from pick import pick
import hashlib
import time
import os
import re


def say_question(title, options, table_name):
    def get_label(option):
        return option.get("name" + table_name)

    option, index = pick(options, title, indicator=">", options_map_func=get_label)
    return option["id"]


def display_message(personne, message):
    print(f"\n<{personne.upper()}>\n{message}\n")


def create_login(firstname, lastname):
    if " " in lastname:
        lastname = lastname.split(" ")[0][0] + lastname.split(" ")[1]

    login = (firstname[0] + lastname).lower()
    count = 0

    while select("joueur", "one", "*", "WHERE login='%s'" % (login)) is not None:
        count += 1
        login = (firstname[0] + lastname).lower() + f"_{count}"

    return login


def first_uppercase_letter(string):
    new_string = []
    if " " in string:
        for section in string.split(" "):
            new_string.append(section.lower()[0].upper() + section.lower()[1:])
        return " ".join(new_string)
    elif "-" in string:
        for section in string.split("-"):
            new_string.append(section.lower()[0].upper() + section.lower()[1:])
        return "-".join(new_string)
    else:
        return string.lower()[0].upper() + string.lower()[1:]


def format_float(floatNumber):
    """
    Permet d'arrondir correctement un nombre à virgule

    `format_float(10.0)`
    """
    if round(floatNumber - int(floatNumber), 2) < 0.05:
        return int(floatNumber)
    else:
        if int(list(str(int(floatNumber * 100)))[-1]) >= 5:
            new_list = []
            new_list.append(
                "".join(list(str(int(floatNumber * 100)))[:-2])
                + str(int(list(str(int(floatNumber * 100)))[-2]) + 1)
            )
            return float("".join(new_list)) / 10
        else:
            return round(floatNumber, 1)
