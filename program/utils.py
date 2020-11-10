import json
import collections
import urllib
import urllib2


def format_gist(description, public, file_name, content):
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


def shorten_url(url):
    """Shorten the gist url.

    Args:
        url (str): Url to be shortened.

    Returns:
        str: Shortened url.
    """
    request_url = "http://tinyurl.com/api-create.php?" + urllib.urlencode({"url": url})
    request = urllib2.Request(request_url)
    response = urllib2.urlopen(request)

    if response.getcode() >= 400:
        return url

    return response.read()
