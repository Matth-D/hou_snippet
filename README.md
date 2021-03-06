# Hou_snippet 

This is a tool for Houdini that allows to generate link to share snippets of nodes between users.
It allows to quickly generate snippet network of the nodes you wish to transfer, serialize them and store them on github gists. 
By sending the generated link or copying a link sent by another user you can serialize/deserialize the nodes from/to your houdini sessions. Allowing for an easy transfer of nodes/scenes between users.
A video demo of the tool is available here: https://vimeo.com/554680574
## 1. Installation

Git clone the repository to your system or, on the repository GitHub page, click the green button Code and download the repository as a zip file.
Unzip and store on your system.
In Houdini, create a new shelf tool. Right click on it and then select "Edit Tool..". In the script tab copy the code below:

```python
import sys
import hou

path = r"Insert path to src folder here."

# example: 
# path = r"C:\Users\Matthieu\Downloads\hou_snippet-main\src"

if path not in sys.path:
    sys.path.append(path)

import hou_snippet.ui


hou_snippet.ui.main()
```

Replace the path to the src folder on your machine next to the path variable as shown.
The tool should now be ready to use.

## 2. How to use

On startup the tool will ask your for a username. It will be stored and sent with the gist data to keep track of the person who sent it.
First you should select the nodes you wish to send then click the Create Snippet button to generate a subnetwork containing those nodes.
Select the snippet subnetwork and hit the Send Snippet to Clipboard button. It will generate a http link and put it straight to your clipboard.
You are now able to paste it in your messaging platform of choice to send other users the snippet contents.
When you receive the link, copy it to your clipboard and then hit the Import Snippet from Clipboard button. It will paste the snippet content directly in your Houdini session.

Received snippet can be access through the Library tab, you can either import them again in your Houdini session or delete them from the UI.

## 3. Notes

On startup the tool will ask for a username and create a ".hou_snippet" folder in your user folder to store your username and received snippets.
The snippet are uploaded to github gist as .json files.
Hou_snippet takes advantage of the Github Actions workflow. It will scan snippets and delete those that are over two days old. The script is triggered every 12th hour, make sure to import the snippet before that time as it will be automatically deleted.