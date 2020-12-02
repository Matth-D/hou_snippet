import base64
import json
import os

import urllib2

auth_file_path = os.path.join(os.path.dirname(__file__), "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)

gist_url = "https://api.github.com/gists/0f2ffce1cc87c490cf99578c65a9afce"


def delete_gist(url):
    request_method = "DELETE"
    b64str = base64.b64encode(
        "{0}:{1}".format(AUTH_DATA["username"], AUTH_DATA["gist_token"])
    )
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic {0}".format(b64str))
    # request.add_header("User-Agent", "Magic Browser")
    request.get_method = lambda: request_method
    response = urllib2.urlopen(request)


delete_gist(gist_url)
# print response.read()
