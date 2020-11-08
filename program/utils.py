import json
import collections


def format_gist(description, public, file_name, content):
    """Return json formatted gist ready for POST.

    Args:
        description (str): Gist description.
        public (bool): Public or private gist.
        file_name (str): Specify file name.
        content (str): Gist content.

    Returns:
        [str]: JSON formatted str from inputs.
    """

    keys = ["description", "public", "files"]
    dict_structure = collections.OrderedDict().fromkeys(keys)
    dict_structure["description"] = description
    dict_structure["public"] = public
    dict_structure["files"] = {file_name: {"content": content}}
    json_output = json.dumps(dict_structure, indent=2, default=str)

    return json_output
