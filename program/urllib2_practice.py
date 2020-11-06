import sys
import os
import json
import urllib
import urllib2
import base64


# libraries = os.path.join(os.path.dirname(__file__), "libraries")

# if libraries not in sys.path:
#     sys.path.append(libraries)
# import requests

auth_file = os.path.join(os.path.dirname(__file__), "auth.json")

with open(auth_file, "r") as auth_file:
    auth_data = json.load(auth_file)

username = auth_data["username"]
full_token = auth_data["full_token"]
gh_api_url = "https://api.github.com"
gh_url = "https://github.com"
usr_gh_url = gh_api_url + "/users/{0}".format(username)

"""Login to Github"""

request = urllib2.Request(usr_gh_url)
b64str = base64.b64encode("{0}:{1}".format(username, full_token))
request.add_header("Authorization", "Basic {0}".format(b64str))
request2 = urllib2.Request(gh_api_url + "/users/houdini-snippet/gists")
response = urllib2.urlopen(request)
response2 = urllib2.urlopen(request2)

print response2.read()

# password_mngr.add_password(None,)


# user = "houdini-snippet"
# request = urllib2.Request("https://api.github.com/users/Matth-D")
# response = urllib2.urlopen(request)
# print response.info()

# gists_url = gh_api_url + "/users/{0}/gists".format(user)

# request = urllib2.Request(gists_url)

# response = urllib2.urlopen(request)

# html = response.read()
