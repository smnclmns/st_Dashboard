import streamlit as st
import os, re

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


st.write("This is the about us page.")

st.link_button("Google Sheet",st.session_state.ch.spreadsheet_url)

try:
    from custom_moduls.calender_widget.helper_functions import months_ahead

    st.write(months_ahead(0))
except Exception as e:
    files_in_exception = find_files_in_exception(e)
    if files_in_exception:
        st.write(f"Exception occurred in the following files: {files_in_exception}")
    else:
        st.write(f"Exception occurred: {e}")
