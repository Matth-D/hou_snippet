import base64
import datetime
import json
import os
import sys
import urllib

from . import utils, utils_hou

GIST_TOKEN = utils.decode_zlib_b64(utils.AUTH_DATA["gist_token"])


def delete_all_gists():
    """Scan all gists and delete ones that are over 2 days old.
    """
    gists_url = "https://api.github.com/users/{}/gists".format(
        utils.AUTH_DATA["username"]
    )
    gists_response = urllib2.urlopen(gists_url, cafile=utils.CERTIF_FILE)
    gists = json.loads(gists_response.read())
    today = datetime.datetime.today()
    gists_list = []

    if not gists:
        print "No gists found."
        return

    for gist in gists:
        gist_date_str = str(gist["description"].split(utils.SEP)[2])
        gist_date_obj = datetime.datetime.strptime(gist_date_str, "%d-%m-%Y")
        limit_date = today - datetime.timedelta(2)

        if gist_date_obj < limit_date:
            gists_list.append(gist["url"])
            print gist["description"]

    b64str = base64.b64encode("{0}:{1}".format(utils.AUTH_DATA["username"], GIST_TOKEN))
    request_method = "DELETE"
    for url in gists_list:
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Magic Browser")
        request.add_header("Authorization", "Basic {0}".format(b64str))
        request.get_method = lambda: request_method
        response = urllib2.urlopen(request, cafile=utils.CERTIF_FILE)


delete_all_gists()
