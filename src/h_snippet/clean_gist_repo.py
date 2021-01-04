import urllib
import urllib2
import json
import os
import base64
import sys

h_snippet = os.path.dirname(__file__)
src = os.path.dirname(h_snippet)
h_snippet_repo = os.path.dirname(src)
libs = os.path.join(h_snippet_repo, "libs")

if libs not in sys.path:
    sys.path.append(libs)

import certifi

auth_file_path = os.path.join(os.path.dirname(__file__), "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)
CERTIF_FILE = certifi.where()

print AUTH_DATA["username"]
print AUTH_DATA["gist_token"]
print CERTIF_FILE

# def delete_all_gists():
#     gists_url = "https://api.github.com/users/houdini-snippet/gists"
#     gists_response = urllib2.urlopen(gists_url, cafile=CERTIF_FILE)
#     gists = json.loads(gists_response.read())
#     gists_list = []

#     if not gists:
#         return
#     for gist in gists:
#         gists_list.append(gist["url"])

#     b64str = base64.b64encode(
#         "{0}:{1}".format(AUTH_DATA["username"], AUTH_DATA["gist_token"])
#     )
#     request_method = "DELETE"
#     for url in gists_list:
#         request = urllib2.Request(url)
#         request.add_header("Authorization", "Basic {0}".format(b64str))
#         request.get_method = lambda: request_method
#         response = urllib2.urlopen(request, cafile=CERTIF_FILE)


# delete_all_gists()
