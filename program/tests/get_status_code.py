import urllib2
import urllib
import sys


gh_url = "http://api.github.com"


request = urllib2.Request(gh_url)
response = urllib2.urlopen(request)

status_code = response.getcode()
print status_code
