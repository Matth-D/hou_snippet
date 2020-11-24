"""H_snippet Core module"""

import base64
import json
import os
import platform
import sys
import tempfile
import urllib
import urllib2

import hou

from . import utils

# CONSTANTS

auth_file_path = os.path.join(os.path.dirname(__file__), "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)
# HOME = os.environ.get("HOME", os.environ.get("USERPROFILE"))
HOME = utils.get_home()
HOU_VER = hou.applicationVersion()[0]
SEP = utils.SEP

# class SnippetPackage:
#     def __init__(self, description, filename, public, content):
#         self.description = description
#         self.filename = filename
#         self.public = public
#         self.content = content


class GitTransfer:
    def __init__(self, *args, **kwargs):
        self.gh_api_url = "https://api.github.com"
        self.gist_api_url = self.gh_api_url + "/gists"
        self.snippet_node = kwargs.pop("snippet_node", None)
        self.snippet_name = None
        self.username = kwargs.pop("username", "default")
        self.public = "True"  # Leaving public gist by default
        self.gist_data = None
        self.separator = r"$#!--%"
        self.content_file = None
        self.content = None

    def create_content(self, snippet):
        self.snippet_name = snippet.name()
        fd, self.content_file = tempfile.mkstemp(suffix=".cpio")
        # When figured out implement switch with saveChildrenToFile() function
        snippet.saveItemsToFile(snippet.children(), self.content_file, False)

        with open(self.content_file, "r") as f:
            self.content = f.read()
        # utils.print_file_head(self.content_file, 5)
        # os.close(self.content_file)

    def create_gist_data(self, username, snippet_name, content):
        description = "Gist containing snippet data for {0} created by {1}.".format(
            snippet_name, username
        )
        filename = utils.create_file_name(snippet_name, username)
        content = utils.encode_zlib_b64(content)
        # print description, type(description)
        # print self.public, type(self.public)
        # print filename, type(filename)
        # print content[:55], type(content)
        # print self.gist_data
        self.gist_data = utils.format_gist_data(
            description, self.public, filename, content
        )
        # FIGURE OUT WHY GIST DATA DOESN'T CONNECT

    def gist_request(self, username, snippet_name, content):
        # Create Gist Request
        # method > POST

        if not self.gist_data:
            return

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
    def send_snippet(self):
        self.create_content(self.snippet_node)
        test_file = os.path.join(os.path.dirname(__file__), "tests", "test_paste.cpio")
        self.format_gist_data(self.username, self.snippet_name, self.content)
        # if os.path.exists(test_file):
        #     print "il existeeee"
        # print testfile
        # with open(testfile, "w") as data:
        #     json.dump("prout", data, indent=4)

    def get_snippet(self):
        pass

    def delete_snippet(self):
        pass


class LocalTransfer:
    def send_snippet(self):
        pass

    def get_snippet(self):
        pass


class Snippet:
    def __init__(self):
        # super(Snippet, self).__init__()
        self.transfer = GitTransfer()
        self.h_snippet_path = os.path.join(HOME, ".h_snippet")
        self.user_file_path = os.path.join(self.h_snippet_path, "user.json")
        self.username = None
        self.local_transfer_switch = None
        self.initialize_user_folder()

    def initialize_user_folder(self):
        """Initialize .h_snippet folder and user files necessary for further use of the tool."""
        if not os.path.exists(self.h_snippet_path):
            os.mkdir(self.h_snippet_path)

        snippet_received_path = os.path.join(self.h_snippet_path, "snippets_received")
        if not os.path.exists(snippet_received_path):
            os.mkdir(snippet_received_path)

        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, "r") as user_file:
                user_data = json.load(user_file)
            self.username = user_data["username"]
            return

        username_prompt = hou.ui.readInput(
            "First usage, please enter username:", ("OK", "Cancel")
        )
        self.username = utils.camel_case(username_prompt[1])

        if not self.username:
            hou.ui.displayMessage("Please enter a valid username")
            sys.exit(1)

        with open(self.user_file_path, "w") as user_file:
            json.dump({"username": self.username}, user_file, indent=4)

    def create_snippet_network(self):
        """Create snippet subnetwork at /obj level for user selection"""
        selection = utils.get_selection(1)

        if not selection:
            hou.ui.displayMessage("Please select nodes to send.")
            return

        obj_context = hou.node("/obj")
        selection_type = selection[0].type().category().name()

        snippet_name_prompt = hou.ui.readInput("Enter snippet name:", ("OK", "Cancel"))
        snippet_name = "snippet_" + snippet_name_prompt[1]

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
        snippet_verif = snippet_subnet.createNode("null")
        snippet_verif.setName("snippet_verification")
        snippet_verif.setDisplayFlag(False)
        snippet_verif.hide(True)
        destination_node.setName("container_" + snippet_name_prompt[1])
        destination_node.setColor(hou.Color(0, 0, 0))

        hou.copyNodesTo(selection, destination_node)

    def send_snippet_to_clipboard(self):
        selection = utils.get_selection(0)

        if not selection or not utils.is_snippet(selection):
            hou.ui.displayMessage(
                "Please select a snippet node network. Must be created with the H_Snippet shelf tool."
            )
            return

        transfer = GitTransfer(snippet_node=selection, username=self.username)

        if self.local_transfer_switch:
            transfer = LocalTransfer()
        # transfer.create_content(selection)
        transfer.send_snippet()


# class classTest:
#     def __init__(self):
#         self.selection = None

#     def print_selection(self):
#         self.selection = utils.get_selection(0)
#         check_selection = utils.is_snippet(self.selection)
#         print check_selection
