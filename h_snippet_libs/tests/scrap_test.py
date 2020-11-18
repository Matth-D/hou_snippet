import datetime
import tempfile
import os
import json


# fd, tempfile = tempfile.mkstemp()

# temp_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}

# with open(tempfile, "w") as tmp:
#     json.dump(temp_dict, tmp, indent=4)

# with open(tempfile, "r") as tmp:
#     content = json.load(tmp)

# print content
# print tempfile

# os.close(fd)
# os.remove(tempfile)

today = datetime.datetime.today()
display = today.strftime("%d-%m-%Y")
print display
