import sys
import os
import json
import urllib
import urllib2
import base64
import zlib


program = os.path.dirname(os.path.dirname(__file__))
utils_path = os.path.join(program, "utils.py")

if utils_path not in sys.path:
    sys.path.append(utils_path)
if program not in sys.path:
    sys.path.append(program)

import utils


auth_file = os.path.join(program, "auth.json")

with open(auth_file, "r") as auth_file:
    auth_data = json.load(auth_file)

"""Request data"""

username = auth_data["username"]
gist_token = auth_data["auth_token"]

gh_api_url = "https://api.github.com"
gh_url = "https://github.com"
gist_api_url = gh_api_url + "/gists"
usr_gh_url = gh_api_url + "/users/{0}".format(username)

gist_name = "created from vscode"
gist_content = "gists body sent from vscode"

savedItems = os.path.join(os.path.dirname(__file__), "savedItems.cpio")
with open(savedItems, "r") as f:
    savedItems_data = f.read()
savedItems_data = utils.encode_zlib_b64(savedItems_data)

# gist_args = utils.format_gist(gist_name, True, "test_gists.py", gist_content)
gist_args2 = utils.format_gist(gist_name, True, "test_gists.py", savedItems_data)
data = gist_args2

"""Create Gist"""

method = "POST"

request = urllib2.Request(gist_api_url, data=data)
b64str = base64.b64encode("{0}:{1}".format(username, gist_token))
request.add_header("Authorization", "Basic {0}".format(b64str))
response = urllib2.urlopen(request)
response_json = response.read()
response_dict = json.loads(response_json)

gist_url = response_dict["url"]

print gist_url
