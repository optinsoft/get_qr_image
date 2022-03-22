import os
import sys
import argparse
import wget
from inputimeout import inputimeout, TimeoutOccurred

def main():
    script_name = "get_qr_image.py"

    parser = argparse.ArgumentParser(description=script_name)

    default_sleep = 5

    parser.add_argument('--url', required=True, help="QR image URL")
    parser.add_argument('--sleep', type=int, default=default_sleep, help="Number of seconds to sleep between repeats. Default: "+str(default_sleep)+" sec.")

    args = parser.parse_args()

    url = args.url
    sleep = args.sleep

    ANDROID_HOME = os.getenv("ANDROID_HOME")
    if (ANDROID_HOME == None):
        print("ANDROID_HOME is not specified")
        return
    emulatorPath = os.path.join(ANDROID_HOME, "emulator")
    resourcesPath = os.path.join(emulatorPath, "resources")
    if not os.path.exists(resourcesPath):
        print("Path does not exist:", resourcesPath)
        return
    targetFilePath  = os.path.join(resourcesPath, 'custom.png')
    downloadFilePath = os.path.join(resourcesPath, 'custom-download.png')
    next = True
    while next:
        try:
            if os.path.exists(downloadFilePath):
                print("Removing:", downloadFilePath)
                os.remove(downloadFilePath)
            print("Downloading:", url, "->", downloadFilePath)
            wget.download(url, downloadFilePath)
            print("\nMoving:", downloadFilePath, "->", targetFilePath)
            os.replace(downloadFilePath, targetFilePath)
        except Exception as ex:
            print(ex)
        try:
            c = inputimeout(prompt='\nDelay '+str(sleep)+' seconds. Type "exit" to quit or any other value to continue.\n', timeout=sleep)
        except TimeoutOccurred:
            c = ""
        if "exit" == c:
            next = False

if __name__ == "__main__":
    main()