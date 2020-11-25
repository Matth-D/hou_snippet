import base64
import json
import os
import sys
import urllib
import urllib2

# import utils

program = os.path.dirname(os.path.dirname(__file__))
utils_path = os.path.join(program, "utils.py")

if utils_path not in sys.path:
    sys.path.append(utils_path)
if program not in sys.path:
    sys.path.append(program)


gist_url = "https://api.github.com/gists/1d8f000371a8b57a279637f00e7ace42"
# short_url = utils.shorten_url(gist_url)
# print short_url
request = urllib2.Request(gist_url)
response = urllib2.urlopen(request)
response_dict = json.loads(response.read())
content = response_dict["files"]["gist"]["content"]
# content_decode = utils.decode_zlib_b64(content)

# loadItems = os.path.join(os.path.dirname(__file__), "loadItems.cpio")

print content[:100]
# with open(loadItems, "wb") as f:
#     f.write(content_decode)


# TODO: FIND A FIX FOR ERROR CODE
# urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
