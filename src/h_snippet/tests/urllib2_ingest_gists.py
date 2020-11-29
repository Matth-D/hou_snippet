import base64
import json
import os
import sys
import timeit
import urllib
import urllib2

# import utils

# program = os.path.dirname(os.path.dirname(__file__))
# utils_path = os.path.join(program, "utils.py")

# if utils_path not in sys.path:
#     sys.path.append(utils_path)
# if program not in sys.path:
#     sys.path.append(program)
shorturl = "https://cutt.ly/ahdFfQX"
long_url = "https://api.github.com/gists/ba83ae76828c07804fd7561df179adc7"
# short_url = utils.shorten_url(gist_url)
# print short_url
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


request = urllib2.Request(shorturl)
# request = HeadRequest(shorturl)
request.add_header("User-Agent", "Magic Browser")
response = urllib2.urlopen(request)
print response.read()
# response_dict = json.loads(response.read())
# content = response_dict["files"]["gist"]["content"]
# print timeit.timeit(response.geturl, number=1000000)
# print response.geturl()

# test.geturl()


# content_decode = utils.decode_zlib_b64(content)

# loadItems = os.path.join(os.path.dirname(__file__), "loadItems.cpio")

# with open(loadItems, "wb") as f:
#     f.write(content_decode)


# TODO: FIND A FIX FOR ERROR CODE
# urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
