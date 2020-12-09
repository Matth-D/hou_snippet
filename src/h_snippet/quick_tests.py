import os
import platform


def check_internet():
    os_name = platform.system().lower()
    ping_cmd = "ping -n 1 8.8.8.8 -w 1"
    if os_name != "windows":
        ping_cmd = "ping -c 1 8.8.8.8 -t 1"

    response = os.system(ping_cmd)

    if response == 0:
        return True
    else:
        return False
