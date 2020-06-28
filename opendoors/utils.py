import html
import os
import re
import shutil
import unicodedata
from os.path import join
from pathlib import Path

from unidecode import unidecode

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


def get_full_path(path):
    return join(path) if Path(path).is_absolute() else join(ROOT_DIR, path)


def copy_to_dir(old_file_path, new_file_dir, new_file_name):
    if not (os.path.exists(new_file_dir)):
        os.makedirs(new_file_dir)
    return shutil.copyfile(old_file_path, os.path.join(new_file_dir, new_file_name))


def make_banner(border_char, banner_text):
    banner_border = border_char.ljust(len(banner_text), border_char)
    return f"\n{banner_border}\n{banner_text}\n{banner_border}"


def create_or_set_working_dir(code_name):
    _working_dir = os.path.join(os.path.expanduser("~"), "otw_opendoors", code_name)
    prompt = input(">> Path to working directory to use for this archive "
                   "(press Enter for default: {}):\n".format(_working_dir))
    if prompt != "":
        _working_dir = prompt

    try:
        if os.path.exists(_working_dir):
            print("Found existing working directory {}".format(_working_dir))
        else:
            os.makedirs(_working_dir)
            print("Successfully created the directory {}".format(_working_dir))

    except OSError as err:
        print("Creation of the directory {} failed: {}".format(_working_dir, err))
        return False
    else:
        return _working_dir


def generate_email(name: str, email: str, archive_long_name: str):
    """
    If no email address is provided, generate an ASCII email address at ao3.org by transliterating the username and
    archive long title
    :param name: the author's original display name
    :param email: the author's current email address
    :param archive_long_name: the long name of the archive being processed
    :return: An ASCII ao3.org email address
    """
    if email:
        return email.strip()
    else:
        user = name.title() + archive_long_name.title()
        return re.sub(r'\W+', '', unidecode(user)) + 'Archive@ao3.org'


def print_progress(current, total, text="stories"):
    """
    Print constantly updating progress text to the command line, in the form `current/total item_name`. Note that this
    increments current, so no need to do that in the calling code.
    :param current: current number
    :param total: total number
    :param text: text to display after the counters
    :return: updated progress text on the same line as the previous print out
    """
    current += 1
    import sys
    sys.stdout.write(f'\r{current}/{total} {text}')
    if current >= total:
        sys.stdout.write("\n")
    sys.stdout.flush()
    return current


def prompt(text):
    return input(text + "\n>>")


def normalize(text):
    return unicodedata.normalize("NFKD", html.unescape(text) or '').strip()
