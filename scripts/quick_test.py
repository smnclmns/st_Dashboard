import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services import Prompter as Prompter


with open(".temp/cwd.txt", "w") as f:
    f.write(Prompter.list_cwd_contents())