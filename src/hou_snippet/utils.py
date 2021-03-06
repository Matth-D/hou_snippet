import collections
import datetime
import json
import os
import platform
import random
import string
import subprocess
import sys
import urllib

import urllib2


def append_external_libs():
    hou_snippet = os.path.dirname(__file__)
    src = os.path.dirname(hou_snippet)
    hou_snippet_repo = os.path.dirname(src)
    libs = os.path.join(hou_snippet_repo, "libs")
    if libs not in sys.path:
        sys.path.append(libs)


append_external_libs()

import certifi  # pylint: disable=wrong-import-position


def get_auth_data():
    program = os.path.dirname(__file__)
    auth_file = os.path.join(program, "auth.json")

    with open(auth_file, "r") as auth_file:
        return json.load(auth_file)


AUTH_DATA = get_auth_data()
CUTTLY_TOKEN = AUTH_DATA["cuttly_token"]
SEP = r"$#!--%"
CERTIF_FILE = certifi.where()


def check_internet():
    """Check internet access.

    Returns:
        [bool]: True or False depending on internet access.
    """
    os_name = platform.system().lower()
    param_attempt = "-n" if os_name == "windows" else "-c"
    param_timeout = "-w" if os_name == "windows" else "-t"
    cmd = ["ping", param_attempt, "1", "8.8.8.8", param_timeout, "1"]
    response = subprocess.call(cmd, shell=False)

    return response == 0


def get_home():
    """Return home folder.

    Returns:
        [str]: Path to home folder.
    """
    home = os.environ.get("home", os.environ.get("USERPROFILE"))
    if sys.version_info.major == 2 and home == os.path.expanduser("~"):
        home = os.environ.get("USERPROFILE")
        return home
    if not home:
        return os.path.expanduser("~")


def create_file_name(snippet_name, username):
    """Create snippet local file name.

    Args:
        snippet_name (str): Snippet name.
        username (str): Sender username.

    Returns:
        str: Local snippet filename.
    """
    date = datetime.datetime.today().strftime("%d-%m-%Y")
    rand_string = "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(10)
    )
    components = (snippet_name, username, date, rand_string)
    return str(SEP.join(components))


def print_file_head(input_file_path, lines):
    file_path = open(input_file_path, "r")
    for i in range(lines):
        line = file_path.readline()
        print line


def is_file_empty(file_path):
    """Check is file is empty.

    Args:
        file_path (str): Path to file to check.

    Returns:
        bool: Boolean True or False if file is empty or not.
    """
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0


def format_gist_data(description, public, content):
    """Return json formatted gist ready for POST.

    Args:
        description (str): Gist description.
        public (bool): Public or private gist.
        file_name (str): Specify file name.
        content (str): Gist content.

    Returns:
        str: JSON formatted str from inputs.
    """
    keys = ["description", "public", "files"]
    dict_structure = collections.OrderedDict().fromkeys(keys)
    dict_structure["description"] = description
    dict_structure["public"] = public
    dict_structure["files"] = {"gist": {"content": content}}

    return json.dumps(dict_structure)
    # return str(dict_structure)


def encode_zlib_b64(input_string):
    """Return encoded input str with zlib then base64.

    Args:
        input_string (str): String to be encoded.

    Returns:
        str: Encoded string.
    """
    return input_string.encode("zlib").encode("base64")


def decode_zlib_b64(input_string):
    """Return decoded input string with base64 then zlib.

    Args:
        input_string (str): String to be decoded.

    Returns:
        str: Decoded string.
    """
    return input_string.decode("base64").decode("zlib")


def camel_case(input_string):
    """Conform user input input_string.

    Args:
        input_string (str): user input input_string.

    Returns:
        str: Conformed input_string.
    """
    input_string = input_string.replace(" ", "_")
    components = input_string.split("_")
    input_string = components[0] + "".join(x.title() for x in components[1:])
    return input_string


def shorten_url(url):
    """Shorten the gist url.

    Args:
        url (str): Url to be shortened.

    Returns:
        str: Shortened url.
    """
    request_url = "http://tinyurl.com/api-create.php?" + urllib.urlencode({"url": url})
    request = urllib2.Request(request_url)
    request.add_header("User-Agent", "Magic Browser")
    response = urllib2.urlopen(request)
    if response.getcode() >= 400:
        return url

    short_url = response.read()

    if "https://" not in short_url:
        return url

    return short_url
