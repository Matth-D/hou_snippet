import urllib
import urllib2
import os
import sys

h_snippet = os.path.dirname(__file__)
src = os.path.dirname(h_snippet)
h_snippet_repo = os.path.dirname(src)

libs = os.path.join(h_snippet_repo, "libs")

if libs not in sys.path:
    sys.path.append(libs)

import certifi

CERTIF_FILE = certifi.where()

ghost_url = "https://api.github.com/gists/42dcd615b5c8ed1bd38b765788f1c895"
# ghost_url = "https://google.com"

try:
    request = urllib2.Request(ghost_url)
    request.add_header("User-Agent", "Magic Browser")
    response = urllib2.urlopen(request, cafile=CERTIF_FILE)
    print response.read()
except urllib2.HTTPError:
    print "couldn't find url"
