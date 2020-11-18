# Importing the required libraries
from __future__ import with_statement
import contextlib

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import sys


# Defining the function to shorten a URL
# Recreate this example
def make_shorten(url):
    request_url = "http://tinyurl.com/api-create.php?" + urlencode({"url": url})
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode("utf-8")


myurl = "https://api.github.com/gists/64a941f66907f433303243eda76dc645"

shorter_myurl = make_shorten(myurl)

