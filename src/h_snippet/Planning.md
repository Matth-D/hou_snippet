DEV PLANNING ON H_SNIPPET TOOL.


-------- CORE

    <!-- - Initialize .h_snippet folder in user folder. -->
        <!-- - If folder not present, ask user for a username. Store the username in #h_snippet/user -->
        <!-- - Two folders > Sent & Received -->
    <!-- - Create OBJ node snippet from selection. -->
        <!-- - Ask User for snippet name. Get node selection, create subnetwork node at obj level copy selection to node -->
          <!-- at obj level. Rename snippet node with user input name. Change color and shape (TBD) -->
    <!-- - Send Snippet to Clipboard: -->
        <!-- - Select snippet and click button.Will create a temp file filled with gist information and the identifier in filename "username_snippetname_date"Then will copy the snippet's children items to that file. -->
          <!-- Upload that file into a gist and return shorten url to clipboard. -->
    <!-- - Import Snippet from Clipboard: -->
        <!-- - Get clipboard content, verify it's a link (hhtps and status code), get the snippets name / sender username / date sent. -->
        <!-- -  Create a file in Received folder -->
        <!-- -  Delete snippet on git -->
    <!-- - Create Two classes. transfer_internet and transfer local. Each with send snippet or get snippet methods. -->
    <!-- - Create a Snippet Class. -->
        <!-- - Inherit send snippet and get snippet methods from transfer classes depending on switch.  -->
          <!-- Leaving room to make the tool local. See dependency injection. -->

    <!-- -add a test if no internet connection -->
        <!-- -if not internet connection no buttons on the ui and just a warning message. Make only Library accessible. -->


    -Handle url not found error in code. Example log:
        "Traceback (most recent call last):
  File "D:\GIT\h_snippet\src\h_snippet\ui.py", line 159, in send_clipboard_to_snippet
    self.snippet.import_snippet_from_clipboard(str(clipboard))
  File "D:\GIT\h_snippet\src\h_snippet\core.py", line 333, in import_snippet_from_clipboard
    clipboard_string=clipboard, snippet_folder=self.snippet_received_path
  File "D:\GIT\h_snippet\src\h_snippet\core.py", line 139, in import_snippet
    if not self.is_link_valid(self.import_url):
  File "D:\GIT\h_snippet\src\h_snippet\core.py", line 201, in is_link_valid
    response = urllib2.urlopen(request, cafile=CERTIF_FILE)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 154, in urlopen
    return opener.open(url, data, timeout)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 435, in open
    response = meth(req, response)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 548, in http_response
    'http', request, response, code, msg, hdrs)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 467, in error
    result = self._call_chain(*args)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 407, in _call_chain
    result = func(*args)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 654, in http_error_302
    return self.parent.open(new, timeout=req.timeout)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 435, in open
    response = meth(req, response)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 548, in http_response
    'http', request, response, code, msg, hdrs)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 473, in error
    return self._call_chain(*args)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 407, in _call_chain
    result = func(*args)
  File "C:\PROGRA~1\SIDEEF~1\HOUDIN~1.173\python27\lib\urllib2.py", line 556, in http_error_default
    raise HTTPError(req.get_full_url(), code, msg, hdrs, fp)
urllib2.HTTPError: HTTP Error 404: Not Found"


-------- UI

    <!-- - One tab called "Snippet" with 3 buttons:  -->
        <!-- - Button Create Snippet from Selection. -->
        <!-- - Button Send Snippet to Clipboard. -->
        <!-- - Button Import Snippet from Clipboard. -->
    <!-- - One tab called "Library":
        -Get clicked item. get clicked item path
        <!-- - List view listing all snippets in .h_snippet folder. -->
            <!-- - columns : Snippet name, sender username, date received. -->
        <!-- - Import button. Import clicked snippet --> -->
    -find a way to keep window on top

-------- UTILS

    <!-- - Copy input str to clipboard. -->
    <!-- - Import clipboard. -->
    <!-- - Create file name for gist from snippet's name, user and today's date. -->

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
    Python NB:
























