"""H_snippet Core module"""

import os
import json
import urllib
import urllib2
import platform
import utils
import hou

# CONSTANTS
program_path = os.path.dirname(__file__)
auth_file_path = os.path.join(program_path, "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)

if platform.system().lower() == "windows":
    HOME = os.environ.get("USERPROFILE")
else:
    HOME = os.path.expanduser("~")


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


def initialize_user_folder():
    """Initialize .h_snippet folder and user files necessary for further use of the tool."""

    h_snippet_path = os.path.join(HOME, ".h_snippet")
    if not os.path.exists(h_snippet_path):
        os.mkdir(h_snippet_path)

    snippet_sent_path = os.path.join(h_snippet_path, "snippets_sent")
    if not os.path.exists(snippet_sent_path):
        os.mkdir(snippet_sent_path)

    snippet_received_path = os.path.join(h_snippet_path, "snippets_received")
    if not os.path.exists(snippet_received_path):
        os.mkdir(snippet_received_path)

    user_file_path = os.path.join(h_snippet_path, "user.json")

    if os.path.exists(user_file_path):
        return

    username_prompt = hou.ui.readInput("Enter username:", ("OK", "Cancel"))
    username = username_prompt[1]
    if not username:
        hou.ui.displayMessage("Please enter a valid username")
        return

    with open(user_file_path, "w") as user_file:
        json.dump({"username": username}, user_file, indent=4)


def create_snippet_network():
    """Create snippet subnetwork at /obj level for user selection"""
    selection = hou.selectedNodes()
    if not selection:
        return
