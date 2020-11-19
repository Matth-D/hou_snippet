import datetime
import json
import os
import tempfile

# fd, tempfile = tempfile.mkstemp(suffix=".cpio")

# temp_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}

# with open(tempfile, "w") as tmp:
#     json.dump(temp_dict, tmp, indent=4)

# with open(tempfile, "r") as tmp:
#     content = json.load(tmp)

# print content
# print tempfile

# os.close(fd)
# os.remove(tempfile)

# today = datetime.datetime.today()
# display = today.strftime("%d-%m-%Y")
# print display

# my_file = open(os.path.normpath("D:\GIT\h_snippet\h_snippet_libs\module2.py"), "r")
# content = my_file.read()
# with open(os.path.normpath("D:\GIT\h_snippet\h_snippet_libs\module2.py"), "r") as f:
#     content = f.read()
# print content

my_file = r"D:\GIT\h_snippet\h_snippet_libs\tests\test_paste.cpio"
with open(my_file, "r") as f:
    content = f.read()

print content
