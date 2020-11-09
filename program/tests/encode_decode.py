import sys
import os

program = os.path.dirname(os.path.dirname(__file__))
utils_path = os.path.join(program, "utils.py")

if utils_path not in sys.path:
    sys.path.append(utils_path)
if program not in sys.path:
    sys.path.append(program)

import utils

mystr = (
    "dbonjouruuuuurrrrrr bbbbbbrbrbrbrberwjjwjwjjj j jjhjh jhjh jh jh jh jh jhhhhhhh"
)

encoded = utils.encode_zlib_b64(mystr)

print encoded
print sys.getsizeof(encoded)

decoded = utils.decode_zlib_b64(encoded)

print decoded
print sys.getsizeof(decoded)
