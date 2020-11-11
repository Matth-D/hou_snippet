"""H_snippet Core module"""

import os
import json
import urllib
import urllib2

# CONSTANTS
program_path = os.path.dirname(__file__)
auth_file_path = os.path.join(program_path, "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)


class SnippetPackage:
    def __init__(self, description, filename, public, content):
        self.description = description
        self.filename = filename
        self.public = public
        self.content = content


# class GitTransfer():
#     def send_snippet():

#     def get_snippet():

# class LocalTransfer():
#     def send_snippet():

#     def get_snippet():

# class Snippet():
#     switch_transfer = 1:
#     self.transfer = GitTransfer()
#     if not switch_transfer:
#         self.transfer = LocalTransfer()

# def initialize_user_folder():
