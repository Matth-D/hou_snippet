# Hou_snippet 

## Installation



```python
import sys
import hou

path = r"insert path to src folder here"

# example: 
# path = r"C:\Users\Matthieu\Downloads\hou_snippet-main\src"

if path not in sys.path:
    sys.path.append(path)

import hou_snippet.ui


hou_snippet.ui.main()
```

## How to use