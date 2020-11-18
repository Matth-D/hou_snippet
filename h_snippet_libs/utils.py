import json
import collections
import urllib
import urllib2
import os
import datetime
import hou

program = os.path.dirname(__file__)
auth_file = os.path.join(program, "auth.json")

with open(auth_file, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)

CUTTLY_TOKEN = AUTH_DATA["cuttly_token"]
SEP = r"$#!--%"
HOU_VER = hou.applicationVersion()[0]


def serialize():
    """if hou<x savechildrentofile else saveItemstoFile need to look it up"""


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
    return SEP.join(components)


def is_file_empty(file_path):
    """Check is file is empty.

    Args:
        file_path (str): Path to file to check.

    Returns:
        bool: Boolean True or False if file is empty or not.
    """
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0


def create_gist_data(description, public, file_name, content):
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
    dict_structure["files"] = {file_name: {"content": content}}
    json_output = json.dumps(dict_structure, indent=2, default=str)

    return json_output


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
