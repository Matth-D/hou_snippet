# Hou_snippet 

## Installation

On the repository GitHub page click the green button Code and download the repository as a zip file.
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

## How to use