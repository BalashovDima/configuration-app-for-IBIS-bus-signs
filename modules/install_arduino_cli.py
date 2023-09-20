import os
import platform
import subprocess
import requests
import shutil

def install_arduino_cli(installation_path):
    '''Downloads arduino cli to specified path

    Returns: True || False, string message saying installation result (successful, error) 
    '''
    current_platform = platform.system().lower()

    if current_platform == "windows":
        # Define the download URL and file paths
        arduino_cli_url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
        download_path = os.path.join(os.getcwd(), "arduino-cli_latest_Windows_64bit.zip")

        try:
            # Download arduino-cli binary
            response = requests.get(arduino_cli_url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Extract arduino-cli.exe to the installation directory
            shutil.unpack_archive(download_path, extract_dir=installation_path)
            # Remove the archive
            os.remove(download_path)
            # Rename LICENSE.txt to arduino-cli-license.txt
            license_path = os.path.join(installation_path, "LICENSE.txt")
            new_license_path = os.path.join(installation_path, "arduino-cli-license.txt")
            os.rename(license_path, new_license_path)

            print(f"Arduino CLI installed to {installation_path}")
            return True, f"Arduino CLI installed to {installation_path}"
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, f"An error occurred: {e}"

    elif current_platform == "linux" or current_platform == "darwin":
        install_cmd = ["sh", "-c", f"curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR={installation_path} sh"]

        try:
            # Run the installation command
            subprocess.run(install_cmd, check=True)
            print(f"Arduino CLI installed to {installation_path}")
            return True, f"Arduino CLI installed to {installation_path}"
        except subprocess.CalledProcessError as e:
            print(f"Error installing Arduino CLI: {e}")
            return False, f"An error occurred: {e}"

    else:
        return False, "Unsupported OS"

if __name__ == '__main__':
    path = input('Path to install arduino-cli to: ')

    install_arduino_cli(path)