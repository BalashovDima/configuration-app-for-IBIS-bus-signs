import subprocess
import json
import re

class LibraryInfo:
    def __init__(self, name, installed, version, latest):
        self.name = name
        self.installed = installed
        self.version = version
        self.latest = latest

def check_arduino_library(library_names, check_latest=False):
    '''Checks if specified arduino library(ies) is(are) installed and compiler sees it(them)

    Arguments: library_names -- iterable of names of the libraries to check || a single string containing library name
    Returns: tuple of object with properties: name (string), installed (bool), version (string || None), latest (string || None) 
    '''
    if isinstance(library_names, str):
        library_names = (library_names,)  # Convert a single string to a tuple

    results = []

    try:
        command = ['arduino-cli', 'lib', 'list', '--all']
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()

        if process.returncode != 0:
            print(f"Error executing command: {' '.join(command)}")
            print(f"Command output: {error}")
            results.append(LibraryInfo(library_name, False, None, None))

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Command output: {e.output.decode('utf-8')}")
        results.append(LibraryInfo(library_name, False, None, None))

    # loop through all the libraries given
    for library_name in library_names:
        installed = False
        installed_version = None
        latest_version = None

        # Parse the output to check if the library is installed and get the installed version
        lines = output.splitlines()
        for line in lines:
            match = re.search(r'^([^0-9\n]+)\s+([\d+.]+)', line)
            if match:
                lib = match.group(1).strip()
                version = match.group(2)
                if lib == library_name:
                    installed = True
                    installed_version = version
                    break

        if not installed:
            results.append(LibraryInfo(library_name, False, None, None))
            continue
        
        if(check_latest):
            try:
                # Get latest version
                command = ['arduino-cli', 'lib', 'search', library_name, '--format', 'json']
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                search_latest_output, error = process.communicate()

                if process.returncode == 0:
                    search_results = json.loads(search_latest_output)

                    for result in search_results['libraries']:
                        if result['name'] == library_name:
                            latest_version = result['latest']['version']
                            break
                else:
                    print(f"Error executing command: {' '.join(command)}")
                    print(f"Command output: {error}")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing JSON: {e}")
                print(f"Command output: {search_latest_output}")

        results.append(LibraryInfo(library_name, True, installed_version, latest_version))

    return tuple(results)

if __name__ == "__main__":
    library_names = ("Wire", "a library", "SPI", "RTClib", "non-existent", "LiquidCrystal")

    # library_names = []
    # while(True):
    #     name = input("Enter library's name or press Enter to continue: ")
    #     if name == '': break

    results = check_arduino_library(library_names)
    for result in results:
        if result.installed:
            print(f"✔ '{result.name}' ✔ is installed.")
            print(f"Version: {result.version}")
            print(f"Latest version available: {result.latest} \n")
        else:
            print(f"✖ '{result.name}' ✖ is NOT installed.")
            print(f"Latest version available: {result.latest} \n")