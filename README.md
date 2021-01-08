# Hou_snippet 

This is a tool for Houdini that allows to generate link to share snippets of nodes.
## Installation

Git clone the repository on your system or, on the repository GitHub page, click the green button Code and download the repository as a zip file.
Unzip and store on your system.
In Houdini, create a new shelf tool. In the script tab copy the code below:

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
The tool should be now ready to use. 

## How to use

First you should select the nodes you wish to send then click the Create Snippet button to generate a subnetwork containing those nodes.
Select the snippet subnetwork and hit the Send Snippet to Clipboard button. It will generate a http link and put it straight to your clipboard.
You are now able to paste it in your messaging platform of choice to send other users the snippet contents.
When you receive the link, copy it to your clipboard and then hit the Import Snippet from Clipboard button. It will paste the snippet content directly in your Houdini session.