"""H_snippet Core module"""

import base64
import json
import os
import sys
import tempfile

import hou
import urllib2

from . import utils

# CONSTANTS

auth_file_path = os.path.join(os.path.dirname(__file__), "auth.json")
with open(auth_file_path, "r") as auth_file:
    AUTH_DATA = json.load(auth_file)
HOME = utils.get_home()
HOU_VER = hou.applicationVersion()[0]
SEP = utils.SEP
CERTIF_FILE = utils.CERTIF_FILE


class LocalTransfer:
    def send_snippet(self):
        pass

    def get_snippet(self):
        pass


class GitTransfer:
    def __init__(self, *args, **kwargs):
        self.gh_api_url = "https://api.github.com"
        self.gist_api_url = self.gh_api_url + "/gists"
        self.snippet_node = None
        self.snippet_name = None
        self.username = kwargs.pop("username", "default")
        self.public = True  # Leaving public gist by default
        self.gist_data = None
        self.fd = None
        self.content_file = None
        self.content = None
        self.created_url = None
        self.snippet_folder = None
        self.import_url = None
        self.response = None
        self.description = None

    def create_content(self, snippet):
        """Save serialized item to temporary file.

        Args:
            snippet (hou.node): Snippet node to serialize.
        """
        self.snippet_name = snippet.name()
        self.fd, self.content_file = tempfile.mkstemp(suffix=".cpio")
        # When figured out implement switch with saveChildrenToFile() function
        snippet.saveItemsToFile(snippet.children(), self.content_file, False)

        with open(self.content_file, "r") as f:
            self.content = f.read()

    def create_gist_data(self, username, snippet_name, content):
        """Format serialized node data to fit gist requirements.

        Args:
            username (str): Sender's username.
            snippet_name (str): Name of snippet to send.
            content (str): Serialized node data.
        """
        self.description = utils.create_file_name(snippet_name, username)
        self.content = utils.encode_zlib_b64(content)
        self.gist_data = utils.format_gist_data(
            self.description, self.public, self.content
        )

    def gist_request(self, payload):
        """Make request through github's gist api to store the snippet.

        Args:
            payload (str): Request data payload.
        """
        if not payload:
            return

        request = urllib2.Request(self.gist_api_url, data=payload)
        b64str = base64.b64encode(
            "{0}:{1}".format(AUTH_DATA["username"], AUTH_DATA["gist_token"])
        )
        request.add_header("Authorization", "Basic {0}".format(b64str))
        response = urllib2.urlopen(request, cafile=CERTIF_FILE)

        if response.getcode() >= 400:
            hou.ui.displayMessage("Could not connect to server")
            return
        response_content = response.read()
        response_dict = json.loads(response_content)
        url = response_dict["url"]
        url = utils.shorten_url(url)
        self.created_url = url

    def string_to_clipboard(self, input_string):
        """Use houdini method to send generated snippet's url to cliboard.

        Args:
            input_string (str): String to copy to clipboard. Would be use for snippet's url here.
        """
        hou.ui.copyTextToClipboard(input_string)

    def send_snippet(self, **kwargs):
        """Method gathering all the different processes to send serialized node to gist."""
        self.snippet_node = kwargs.pop("snippet_node", None)
        self.create_content(self.snippet_node)
        self.create_gist_data(self.username, self.snippet_name, self.content)
        self.gist_request(self.gist_data)
        self.string_to_clipboard(self.created_url)
        os.close(self.fd)
        os.remove(self.content_file)

    def import_snippet(self, *args, **kwargs):
        """Method gathering all the different processes to import gist url in Houdini."""
        # get clipboard link
        # check clipboard link move the check process in a method here
        self.import_url = kwargs.pop("clipboard_string", None)
        self.snippet_folder = kwargs.pop("snippet_folder", None)
        if not self.is_link_valid(self.import_url):
            return
        self.extract_data()
        self.store_snippet()
        self.delete_snippet()
        # create subnetwork in obj context
        # load content from file stored on disc
        # update tree view?

    def create_import_network(self):
        """Create Snippet network to load imported gist content to."""
        obj_context = hou.node("/obj")
        snippet_subnet = obj_context.createNode("subnet")
        snippet_subnet.setName(snippet_name)
        snippet_subnet.setColor(hou.Color(0, 0, 0))
        # FINISHTHATSHIT
        pass

    def delete_snippet(self):
        """Delete imported gist from gist repo.
        """
        request_method = "DELETE"
        b64str = base64.b64encode(
            "{0}:{1}".format(AUTH_DATA["username"], AUTH_DATA["gist_token"])
        )
        request = urllib2.Request(self.import_url)
        request.add_header("Authorization", "Basic {0}".format(b64str))
        request.get_method = lambda: request_method
        response = urllib2.urlopen(request)

    def store_snippet(self):
        """Store snippet content on disk.
        """
        self.content_file = os.path.join(
            self.snippet_folder, self.description + ".json"
        )

        with open(self.content_file, "w") as snippet_f:
            snippet_f.write(self.content)

    def is_link_valid(self, url):
        """Check if link imported from clipboard is valid and points to a gist.

        Args:
            url (str): String imported from clipboard.

        Returns:
            bool : True or False and set the instance variable of imported link.
        """
        if not url:
            hou.ui.displayMessage("Clipboard is empty")
            return False
        if "https://" not in url:
            hou.ui.displayMessage("Clipboard content not a url link.")
            return False
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Magic Browser")
        response = urllib2.urlopen(request, cafile=CERTIF_FILE)
        if response.getcode() >= 400:
            hou.ui.displayMessage("Url server issue")
            return False
        response_url = response.geturl()
        self.import_url = response_url
        if "github.com/gists" not in response_url:
            hou.ui.displayMessage("Url not pointing to a snippet file")
            return False
        self.response = response
        return True

    def extract_data(self):
        """Extract gist data from gist url response.
        """
        self.gist_data = json.loads(self.response.read())
        self.description = self.gist_data["description"]
        self.content = utils.decode_zlib_b64(self.gist_data["files"]["gist"]["content"])


class Snippet:
    def __init__(self):
        # super(Snippet, self).__init__()
        self.h_snippet_path = os.path.join(HOME, ".h_snippet")
        self.user_file_path = os.path.join(self.h_snippet_path, "user.json")
        self.snippet_received_path = os.path.join(
            self.h_snippet_path, "snippets_received"
        )
        self.username = None
        self.local_transfer_switch = None
        self.initialize_user_folder()
        self.switch_transfer_method = 1
        self.transfer = None
        self.initialize_transfer()

    def initialize_user_folder(self):
        """Initialize .h_snippet folder and user files necessary for further use of the tool."""
        if not os.path.exists(self.h_snippet_path):
            os.mkdir(self.h_snippet_path)

        if not os.path.exists(self.snippet_received_path):
            os.mkdir(self.snippet_received_path)

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

    def initialize_transfer(self):
        """Set the appropriate transfer method based on switch_transfer_method variable."""

        self.transfer = LocalTransfer()
        if self.switch_transfer_method:
            self.transfer = GitTransfer(username=self.username)

    def create_snippet_network(self):
        """Create snippet subnetwork at /obj level for user selection"""
        selection = utils.get_selection(1)

        if not selection:
            hou.ui.displayMessage("Please select nodes to send.")
            return

        obj_context = hou.node("/obj")
        selection_type = selection[0].type().category().name()

        snippet_name_prompt = hou.ui.readInput("Enter snippet name:", ("OK", "Cancel"))
        input_name = snippet_name_prompt[1]
        input_name = input_name.replace(" ", "_")
        snippet_name = "snippet_" + input_name

        if not snippet_name:
            hou.ui.displayMessage("Please enter a snippet name")
            return

        snippet_subnet = obj_context.createNode("subnet")
        snippet_subnet.setName(snippet_name)
        snippet_subnet.setColor(hou.Color(0, 0, 0))

        if HOU_VER >= 16:
            snippet_subnet.setUserData("nodeshape", "wave")
        destination_node = snippet_subnet

        if selection_type == "Object":
            selection.setName("container_" + input_name)

        if selection_type == "Sop":
            destination_node = snippet_subnet.createNode("geo")
            destination_node.setName("container_" + input_name)

        if selection_type == "Vop":
            destination_node = snippet_subnet.createNode("matnet")
            destination_node.setName("container_" + input_name)

        if selection_type == "Driver":
            destination_node = snippet_subnet.createNode("ropnet")
            destination_node.setName("container_" + input_name)

        snippet_verif = snippet_subnet.createNode("null")
        snippet_verif.setName("snippet_verification")
        snippet_verif.setDisplayFlag(False)
        snippet_verif.hide(True)
        destination_node.setColor(hou.Color(0, 0, 0))

        hou.copyNodesTo(selection, destination_node)

    def send_snippet_to_clipboard(self):
        """Method connected to UI's send snippet to clipboard button."""
        selection = utils.get_selection(0)

        if not selection or not utils.is_snippet(selection):
            hou.ui.displayMessage(
                "Please select a snippet node network. Must be created with the H_Snippet shelf tool."
            )
            return

        self.transfer.send_snippet(snippet_node=selection)

    def import_snippet_from_clipboard(self, clipboard):
        """Method connected to UI's import snippet from clipboard button.

        Args:
            clipboard (str): String content of clipboard.
        """

        self.transfer.import_snippet(
            clipboard_string=clipboard, snippet_folder=self.snippet_received_path
        )
        # request = urllib2.Request(clipboard)
        # request.add_header("User-Agent", "Magic Browser")
        # response = urllib2.urlopen(request, cafile=CERTIF_FILE)
        # print response.read()