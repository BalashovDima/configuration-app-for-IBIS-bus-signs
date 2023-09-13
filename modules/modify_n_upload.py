import subprocess
import threading
import time
import customtkinter as ctk
from .modify_arduino_file import modify_arduino_file

'''
Modifies specified arduino sketch and uploads it (compilation is done automaticaly)

Return a list of lines that are the output from arduino-cli

Arguments: file_path -- path to arduino file; data -- data object with all the information needed to modify the sketch; com -- com port in format 'COM<number>'; fqbn -- fqbn of the board connected to the port; inprogress_label_var -- label that is used to indicate that upload is in progress; window -- upload window ctkinter object, it is needed to keep the ui updated (not frozen)
'''
def modify_n_upload(file_path, data, com, fqbn, inprogress_label_var, window):
    modify_arduino_file(file_path, data)

    upload_command = f"arduino-cli upload -p {com} --fqbn {fqbn} {file_path} -v"
    upload_process = subprocess.Popen(upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = []

    def read_upload_output(output):
        for line in upload_process.stdout:
            print(f"Upload: {line.strip()}")
            output.append(line)
        for line in upload_process.stderr:
            print(f"Upload Error: {line.strip()}")
            output.append(line)

    # Start a thread to read and print the upload output and errors
    upload_output_thread = threading.Thread(target=read_upload_output, args=[output])
    upload_output_thread.start()

    # Periodically print dots to indicate ongoing process
    counter = 0
    while upload_process.poll() is None:
        print(".", end="", flush=True)
        text = ''
        if counter == 0:
            text = '⦿'
        elif counter == 1:
            text = '⦿⦿'
        elif counter == 2:
            text = '⦿⦿⦿'
        counter = (counter + 1) % 3
        inprogress_label_var.set(text)
        window.update()
        time.sleep(0.3)
    inprogress_label_var.set('')

    # Wait for the output threads to finish
    upload_output_thread.join()

    return output