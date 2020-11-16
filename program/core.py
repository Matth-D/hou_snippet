"""H_snippet Core module"""

import os
import json
import urllib
import urllib2
import base64
import platform
import collections
import utils
import hou

# CONSTANTS

auth_file_path = os.path.join(os.path.dirname(__file__), "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)
HOME = os.path.expanduser("~")
HOU_VER = hou.applicationVersion()[0]


# class SnippetPackage:
#     def __init__(self, description, filename, public, content):
#         self.description = description
#         self.filename = filename
#         self.public = public
#         self.content = content


class GitTransfer:
    def __init__(self):
        self.gh_api_url = "https://api.github.com"
        self.gist_api_url = self.gh_api_url + "/gists"
        self.public = True  # Leaving public gist by default
        self.gist_data = None
        self.separator = r"$#!--%"

    def create_data(self, username, snippet_name, content):
        description = "Gist containing snippet data for {0} created by {1}.".format(
            snippet_name, username
        )
        filename = utils.create_file_name(snippet_name, username)
        content = utils.encode_zlib_b64(content)
        self.gist_data = utils.create_gist_data(description, self.public, filename)

    def send_snippet(self, username, snippet_name, content):

        # Set all gist data variables

        # Create Gist Request
        # method > POST
        request = urllib2.Request(self.gist_api_url, data=self.gist_data)
        b64str = base64.b64encode(
            "{0}:{1}".format(AUTH_DATA["username"], AUTH_DATA["gist_token"])
        )
        request.add_header("Authorization", "Basic {0}".format(b64str))
        response = urllib2.urlopen(request)

        if response.getcode() >= 400:
            hou.ui.displayMessage("Could not connect to server")
            return
        response_content = response.read()
        response_dict = json.loads(response_content)
        created_gist_url = response_dict["url"]
        return created_gist_url

    #    request = urllib2.Request(gist_api_url, data=gist_data)

    def get_snippet():
        pass

    def delete_snippet():
        pass


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
    if HOU_VER >= 16:
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
