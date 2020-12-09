import os
import platform


def check_internet():
    os_name = platform.system().lower()
    ping_cmd = "ping -n 1 8.8.8.8"
    if os_name != "windows":
        ping_cmd = "ping -c 1 8.8.8.8"
    response = os.system(ping_cmd)

    if response == 0:
        print "Internet active"
    else:
        print "No Internet"


check_internet()
