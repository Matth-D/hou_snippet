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

GIST_USERNAME = AUTH_DATA["username"]
GIST_TOKEN = AUTH_DATA["gist_token"]

if platform.system().lower() == "windows":
    HOME = os.environ.get("USERPROFILE")
else:
    HOME = os.path.expanduser("~")

HOU_VER = hou.applicationVersion()[0]


class SnippetPackage:
    def __init__(self, description, filename, public, content):
        self.description = description
        self.filename = filename
        self.public = public
        self.content = content


# class GitTransfer():
#     def __init__(self, snippet_data):
#         self.snippet_data = snippet_data

#     def send_snippet(snippet_data):

#     def get_snippet():

#     def delete_snippet():

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

    snippet_received_path = os.path.join(h_snippet_path, "snippets_received")
    if not os.path.exists(snippet_received_path):
        os.mkdir(snippet_received_path)

    user_file_path = os.path.join(h_snippet_path, "user.json")

    if os.path.exists(user_file_path):
        return

    username_prompt = hou.ui.readInput("Enter username:", ("OK", "Cancel"))
    username = utils.camel_case(username_prompt[1])

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
    obj_context = hou.node("/obj")
    selection_type = selection[0].type().category().name()

    snippet_name_prompt = hou.ui.readInput("Enter snippet name:", ("OK", "Cancel"))
    snippet_name = snippet_name_prompt[1]

    if not snippet_name:
        hou.ui.displayMessage("Please enter a snippet name")
        return
    snippet_name = snippet_name.replace(" ", "_")

    snippet_subnet = obj_context.createNode("subnet")
    snippet_subnet.setName(snippet_name)
    snippet_subnet.setColor(hou.Color(0, 0, 0))
    snippet_subnet.setUserData("nodeshape", "wave")
    destination_node = snippet_subnet

    if selection_type == "Sop":
        destination_node = snippet_subnet.createNode("geo")

    if selection_type == "Vop":
        destination_node = snippet_subnet.createNode("matnet")

    if selection_type == "Driver":
        destination_node = snippet_subnet.createNode("ropnet")

    destination_node.setName(snippet_name)

    hou.copyNodesTo(selection, destination_node)
