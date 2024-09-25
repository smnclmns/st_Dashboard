import streamlit as st
import os, re, traceback
from custom_moduls.calender_widget.helper_functions import months_ahead

def find_files_in_exception(exception):

    cwd = os.getcwd()
    root_folder = os.path.dirname(cwd)
    
    # Extract file paths from the exception message using regex
    file_paths_in_exception = re.findall(r'([a-zA-Z]:[\\\w.\\-]+|/[^:\s]+)', str(exception))

    files_in_exception = []
    
    for root, dirs, files in os.walk(cwd):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path in path for path in file_paths_in_exception):

                files_in_exception.append(file_path)

    rel_file_paths = [path.split(root_folder, 1)[1] for path in files_in_exception]
    
    return files_in_exception

def get_file_contents(filepaths: list[str]) -> list[str]:

    file_contents = []
    for path in filepaths:
        with open(path, 'r') as f:
            file_contents.append(f.read())

    return file_contents

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

def get_prompt(cwd_contents: str, files: list[str], file_contents: list[str], exception_msg: str):
    prompt = ""

    prompt += f"My project:\n`{cwd_contents}`\n\n"

    for file, content in zip(files, file_contents):

        prompt += f"{file}:\n`{content}`\n"

    prompt += f"Error:\n`{exception_msg}`"

    return prompt


st.write("This is the about us page.")

st.link_button("Google Sheet",st.session_state.ch.spreadsheet_url)

try:

    st.write(months_ahead(0))
except:
    files_in_exception = find_files_in_exception(traceback.format_exc())
    if files_in_exception:
        st.write(f"Exception occurred in the following files: {files_in_exception}")

        prompt = get_prompt(
            list_cwd_contents(),
            files_in_exception,
            get_file_contents(files_in_exception),
            traceback.format_exc())
        
        st.write(prompt)

        with open("prompt.txt", "w") as f:
            f.write(prompt)

    else:
        st.write(traceback.format_exc())
