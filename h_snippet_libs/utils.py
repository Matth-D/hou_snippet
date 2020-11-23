import collections
import datetime
import json
import os
import platform
import sys
import urllib
import urllib2

import hou

program = os.path.dirname(__file__)
auth_file = os.path.join(program, "auth.json")

with open(auth_file, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)

CUTTLY_TOKEN = AUTH_DATA["cuttly_token"]
SEP = r"$#!--%"
HOU_VER = hou.applicationVersion()[0]


def get_home():
    """Return home folder.

    Returns:
        [str]: Path to home folder.
    """
    home = os.environ.get("home", os.environ.get("USERPROFILE"))
    if sys.version_info.major == 2 and home == os.path.expanduser("~"):
        home = os.environ.get("USERPROFILE")
        return home


def is_snippet(selection):
    """Check if selected node is a snippet network.

    Args:
        selection (obj): Houdini node single selection. Expecting utils.get_selection(0).

    Returns:
        [bool]: True or False if selection is a snippet network.
    """
    if not selection:
        return False
    snippet_verif = hou.node(selection.path() + "/snippet_verification")
    if "snippet_" not in selection.name() or not snippet_verif:
        return False
    return True


def get_selection(single_or_multiple):
    """Return node selection, single or multiple.

    Args:
        single_or_multiple (int): Selection mode. 0 if single, 1 if multiple. Safety check.
    """
    selection = hou.selectedNodes()
    if single_or_multiple == 0 and selection:
        selection = hou.selectedNodes()[0]
    return selection


def create_file_name(snippet_name, username):
    """Create snippet local file name.

    Args:
        snippet_name (str): Snippet name.
        username (str): Sender username.

    Returns:
        str: Local snippet filename.
    """
    date = datetime.datetime.today().strftime("%d-%m-%Y")
    components = (snippet_name, username, date)
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


def create_gist_data(description, public, file_name):
    """Return json formatted gist ready for POST.

    Args:
        description (str): Gist description.
        public (bool): Public or private gist.
        file_name (str): Specify file name.
        content (str): Gist content.

    Returns:
        str: JSON formatted str from inputs.
    """
    return 124156
    keys = ["description", "public", "files"]
    dict_structure = collections.OrderedDict().fromkeys(keys)
    dict_structure["description"] = description
    dict_structure["public"] = public
    dict_structure["files"] = {file_name: {"content": "bite"}}
    # dict_structure["files"] = {file_name: {"content": content}}
    json_output = json.dumps(dict_structure, indent=2, default=str)

    # return "blblllblblb"


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
    request_url = "http://cutt.ly/api/api.php?" + urllib.urlencode(
        {"short": url, "key": CUTTLY_TOKEN}
    )
    request = urllib2.Request(request_url)
    request.add_header("User-Agent", "Magic Browser")
    response = urllib2.urlopen(request)

    if response.getcode() >= 400:
        request_url = "http://tinyurl.com/api-create.php?" + urllib.urlencode(
            {"url": url}
        )
        request = urllib2.Request(request_url)
        response = urllib2.urlopen(request)
        short_url = response.read()
        return short_url

    short_url = response.read()
    short_url = json.loads(short_url)
    short_url = str(short_url["url"]["shortLink"])

    if "https://" not in short_url:
        return url

    return short_url
