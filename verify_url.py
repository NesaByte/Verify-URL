# Tool Name: Verify URL
# Tool Author: Andre Bhaseen
# Version: 0.1
# Liscence: MIT Liscence
# Description: A Tool used to verify the return code of a URL

import requests  # used for receiving requests codes
import argparse  # used for parsing customized command line arguemnts
import sys  # used for grabbing command line argmuents
# import codecs #originally used for parsing...

# Using beautiful soup for parsing HTML
# Setting up Beautiful Soup

import bs4 as bs
import urllib.request

# Setting up colors for output
# Grabbed code from here: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python # The origin of the code however is from Blender


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ORANGEWARNING = '\033[38;5;214m'
    INFOCYAN = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Setting up range for request codes
# last number in range is not included - range in python works as: [m,n)

# Informational
informationalCode = range(100, 200)
# Success code range
successCode = range(200, 300)
# Redirection
redirectCode = range(300, 400)
# Error code range
errorCode = range(400, 500)
# Server Error range
serverErrorCode = range(500, 600)

# Creating an array to store URLs
urls = []

# Testing URLs:
# urls.append('http://google.com')  # 200
# urls.append('http://google.com/nothere')  # 404
# urls.append('http://api.github.com/user')  # 401

# Main Component of Program


def main(singleUrl, version, filename):
    if version is True:
        print(
            f"{bcolors.HEADER}Verify URL Tool {bcolors.ENDC} Version: {bcolors.BOLD}0.1{bcolors.ENDC}")
    elif singleUrl == "const":
        print(
            f"{bcolors.WARNING}⚠️ URL has not been entered, please enter a URL after the -u/--url argument to analyze.{bcolors.ENDC}")
    else:
        if singleUrl != "default" and singleUrl != "const":
            urls.append(singleUrl)
        elif (filename):
            if (filename[0].endswith(".html")):
                with open(filename[0], 'r') as f:
                    source = f.read()
                    soup = bs.BeautifulSoup(source, 'lxml')
                for url in soup.find_all('a'):
                    urls.append(url.get_text('href'))
            else:
                print(f"{bcolors.WARNING}⚠️ File should be in HTML format, for single URLs please use the -u/--url arguments before the URL.{bcolors.ENDC}")
        else:
            if len(sys.argv) == 1:
                parser.print_help(sys.stderr)
                sys.exit(1)
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                # print(r.status_code) #used for testing purposes
                if r.status_code in successCode:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.OKGREEN}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.OKGREEN} - Success, this site exists! ✔️{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
                elif r.status_code in errorCode:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.FAIL}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.FAIL} - Failed to reach this site. ❌{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
                elif r.status_code in redirectCode:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.OKBLUE}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.OKBLUE} - This site will redirect you. ↩{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
                elif r.status_code in serverErrorCode:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.ORANGEWARNING}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.ORANGEWARNING} - Encountered a server error. 🚫{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
                elif r.status_code in informationalCode:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.INFOCYAN}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.INFOCYAN} - Informational return code ℹ️{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
                else:
                    print(
                        f"{bcolors.WARNING}Status Code:{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.WARNING} - Unknown Return Code ⚠️{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
            except requests.exceptions.Timeout:
                r.status_code = "Read Timed Out"
                print(
                    f"{bcolors.WARNING}Status Code:{bcolors.FAIL}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.FAIL} - Failed to reach this site. Read Timed Out. ❌{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
            except requests.exceptions.ConnectionError as e:
                r.status_code = "Connection refused"
                print(
                    f"{bcolors.WARNING}Status Code:{bcolors.FAIL}{bcolors.BOLD}{r.status_code}{bcolors.ENDC}{bcolors.FAIL} - Failed to reach this site. Connection Refused. ❌{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            except:
                print("Unexpected Error")


# adding ability to add arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tool used for verifyinig the return code of a URL',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Details information about the tool (version and name of tool)',
        required=False,
        dest='version'
    )
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        nargs='?',
        default='default',
        const='const',
        help='Used for single urls',
        required=False,
        dest='singleUrl'
    )
    args, filename = parser.parse_known_args()
    #args = parser.parse_args()
    main(args.singleUrl, args.version, filename)
