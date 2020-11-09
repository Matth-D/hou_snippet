import sys
import os
import json
import urllib
import urllib2
import base64

program = os.path.dirname(os.path.dirname(__file__))
utils_path = os.path.join(program, "utils.py")

if utils_path not in sys.path:
    sys.path.append(utils_path)
if program not in sys.path:
    sys.path.append(program)

import utils


gist_url = "https://api.github.com/gists/64a941f66907f433303243eda76dc645"

request = urllib2.Request(gist_url)
response = urllib2.urlopen(request)
response_dict = json.loads(response.read())
content = response_dict["files"]["test_gists.py"]["content"]
content_decode = utils.decode_zlib_b64(content)

loadItems = os.path.join(os.path.dirname(__file__), "loadItems.cpio")

with open(loadItems, "wb") as f:
    f.write(content_decode)
