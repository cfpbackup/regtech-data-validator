import os
import sys

CURR_DIR = os.path.dirname(os.path.abspath(__file__)) # noqa: E402
PARENT_DIR = os.path.dirname(CURR_DIR) # noqa: E402
sys.path.append(CURR_DIR) # noqa: E402
sys.path.append(PARENT_DIR) # noqa: E402