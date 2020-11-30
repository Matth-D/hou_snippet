import os
import ssl
import sys

import urllib2
import utils

ssl._create_default_https_context = ssl._create_unverified_context


h_snippet = os.path.dirname(__file__)
src = os.path.dirname(h_snippet)
h_snippet_repo = os.path.dirname(src)
libs = os.path.join(h_snippet_repo, "libs")

if libs not in sys.path:
    sys.path.append(libs)

import certifi

cert_file = certifi.where()
shorturl = "https://cutt.ly/ahdFfQX"
long_url = "https://api.github.com/gists/ba83ae76828c07804fd7561df179adc7"


request = urllib2.Request(shorturl)
request.add_header("User-Agent", "Magic Browser")
response = urllib2.urlopen(request, cafile=cert_file)
print response.read()

