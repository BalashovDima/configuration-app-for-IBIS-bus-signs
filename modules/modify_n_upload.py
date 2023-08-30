import subprocess
from .modify_arduino_file import modify_arduino_file

def modify_n_upload(file_path, data, comport, fqbn):
    modify_arduino_file(file_path, data)

    compile_output = subprocess.run(
        ["arduino-cli", "compile", "--fqbn", fqbn, file_path],
        capture_output=True,
        text=True,
    )
    
    print(compile_output.stdout)

    upload_output = subprocess.run(
        ["arduino-cli", "upload", "-p", comport, "--fqbn", fqbn, file_path],
        capture_output=True
    )

    print(upload_output.stdout)