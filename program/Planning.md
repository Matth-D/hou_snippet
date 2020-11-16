DEV PLANNING ON H_SNIPPET TOOL.


-------- CORE

    ######- Initialize .h_snippet folder in user folder.
    ######    - If folder not present, ask user for a username. Store the ######username in .######h_snippet/user
    ######    - Two folders > Sent & Received
    ######- Create OBJ node snippet from selection.
    ######    - Ask User for snippet name. Get node selection, create ######subnetwork node at obj ######level, copy selection to node
    ######      at obj level. Rename snippet node with user input name. ######Change color and shape ######(TBD)
    - Send Snippet to Clipboard:
        - Select snippet and click button.Will create a temp file filled with gist information and the identifier in filename "username_snippetname_date"Then will copy the snippet's children items to that file.
          Upload that file into a gist and return shorten url to clipboard.
    - Import Snippet from Clipboard:
        - Get clipboard content, verify it's a link (hhtps and status code), get the snippets name / sender username / date sent.
        -  Create a file in Received folder
        -  Delete snippet on git
    - Create Two classes. transfer_internet and transfer local. Each with send snippet or get snippet methods.
    - Create a Snippet Class.
        - Inherit send snippet and get snippet methods from transfer classes depending on switch. 
          Leaving room to make the tool local. See dependency injection.

-------- UI

    - One tab called "Snippet" with 3 buttons: 
        - Button Create Snippet from Selection.
        - Button Send Snippet to Clipboard.
        - Button Import Snippet from Clipboard.
    - One tab called "Library":
        - List view listing all snippets in .h_snippet folder.
            - columns : Snippet name, sender username, date received.
        - Import button. Import clicked snippet

-------- UTILS

    - Copy input str to clipboard.
    - Import clipboard.
    - Create file name for gist from snippet's name, user and today's date.

-------- NOTES

    Snippet I/O:
        Send:
            Inputs:
                - Github credentials from auth.json file.
                - A content > NodeItems.cpio file from Houdini.
                - A description > username - date - name.
                - Public True or False > Default to False.
                - A file name > could be name of snippet + random seed to avoid duplicates.
            Output:
                - URL to snippet on github.gists, shortened by default.
        Get:
            Input:
                - Snippet URL
            Output:
                - Content of downloaded snippet.
                - Description > sender username - date - name

    To Solve:
        - sop type = "Sop" material type = "Vop" mantra node = "Driver"
           if node type != "Sop" create appropriate network to store the nodes.
    Python NB:
        Get node type name = node.type().category().name()