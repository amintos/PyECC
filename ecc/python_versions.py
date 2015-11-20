
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    try:
        from .python_version2 import *
    except ImportError:
        from  python_version2 import *
elif PY3:
    try:
        from .python_version3 import *
    except ImportError:
        from  python_version3 import *
else:
    raise ValueError("This should be either Python version 2 or Python version 3.")
