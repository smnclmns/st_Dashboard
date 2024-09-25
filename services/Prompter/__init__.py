import os, re, traceback

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

def write_prompt_in_txt_file() -> None:

    cwd_contents = list_cwd_contents()
    exception_message = traceback.format_exc()

    files = find_files_in_exception(exception_message)
    file_contents = get_file_contents(filepaths=files)

    prompt = get_prompt(
        cwd_contents=cwd_contents,
        files=files,
        file_contents=file_contents,
        exception_msg=exception_message
    )

    with open("prompt.txt", "w") as f:
        f.write(prompt)
