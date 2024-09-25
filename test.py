import os
import re

def list_cwd_contents():
    cwd = os.getcwd()
    contents = []
    for root, dirs, files in os.walk(cwd):
        if 'venv' in root or '.git' in root:
            continue
        level = root.replace(cwd, '').count(os.sep)
        indent = ' ' * 4 * (level)
        contents.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            contents.append(f"{sub_indent}{f}")
    return "\n".join(contents)

def find_files_in_exception(exception):

    print(exception)
    cwd = os.getcwd()
    files_in_exception = []
    
    # Extract file paths from the exception message using regex
    file_paths_in_exception = re.findall(r'([a-zA-Z]:[\\\w.\\-]+|/[^:\s]+)', str(exception))
    
    for root, dirs, files in os.walk(cwd):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path in path for path in file_paths_in_exception):
                files_in_exception.append(file_path)
    
    return files_in_exception

try:
    from custom_moduls.Connection_handling import Connection_Handler
except Exception as e:
    files_in_exception = find_files_in_exception(e)
    if files_in_exception:
        print(f"Exception occurred in the following files: {files_in_exception}")
    else:
        print(f"Exception occurred: {e}")