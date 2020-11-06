import sys
import os

libraries = os.path.join(os.path.dirname(__file__), "libraries")

if libraries not in sys.path:
    sys.path.append(libraries)

import requests
import hou

test = requests.get("https://api.github.com/")
