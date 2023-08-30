import subprocess
from .modify_arduino_file import modify_arduino_file

def modify_n_upload(file_path, data, com, fqbn):
    modify_arduino_file(file_path, data)

    output = ''

    compile_output = subprocess.run(
        ["arduino-cli", "compile", "--fqbn", fqbn, file_path],
        capture_output=True,
        text=True
    ).stdout
    output += ''.join(compile_output.splitlines()[:2]) + '\n\n'

    upload_output = subprocess.run(
        ["arduino-cli", "upload", "-p", com, "--fqbn", fqbn, file_path],
        capture_output=True,
        text=True
    ).stdout
    output += upload_output

    return output