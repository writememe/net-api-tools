"""
This application will compare the running configuration against
the startup configuration and print the difference to the screen.

To adjust this to your environment, please change the `url` variable
 within the code.

To execute this code, please run the following command:

python ios-config-diff-report.py --help

This will display what are the options to execute the application.
"""

# Import modules
import requests
import pprint
from requests.exceptions import HTTPError
from colorama import Fore, init
import argparse

# Auto-reset colorama colours back after each print statement
init(autoreset=True)

# Setup argparse parameters to take user input from the command line
parser = argparse.ArgumentParser(
    description="Validate startup and running config differences on Cisco devices."
)
parser.add_argument(
    "--host",
    action="store",
    help="Specify the hostname to be queried i.e. lab-host-01.lab.local",
    type=str,
)
# Add debug argument, set to False by default unless required
parser.add_argument(
    "--debug",
    action="store_true",
    help="Provide additional debugging output. True for debugging, set to False by default",
)
args = parser.parse_args()

print(Fore.CYAN + f"Validating config differences on {args.host}")
# Take argparse input and assign to the hostname variable
hostname = args.host
# Define variables
# Define the URL
url = "http://10.0.0.54:5000"
# Define the API path
api_path = "/api/v1/nr/scrapli/genie/host?host="
command_api_path = "&command="
# The command to be parsed.
command = "show archive config differences nvram:startup-config system:running-config"
# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

# Try/except block to validate a successful HTTP response code
try:
    # If debug is set to True, provide the full API call string
    if args.debug is True:
        print(
            Fore.MAGENTA
            + f"Attempting API call - {url}{api_path}{hostname}{command_api_path}{command}"
        )
    # Get the results of the API call
    req = requests.get(url + api_path + hostname + command_api_path + command)
    # If debug is set to True, printout the status code and the raw text response
    if args.debug is True:
        print(Fore.MAGENTA + f"Response code - {req.status_code}")
        print(Fore.MAGENTA + f"Response raw text - {req.text}")
    # If the response was successful, no exception will be raised
    req.raise_for_status()
# Raise exception, print HTTP error
except HTTPError as http_err:
    print(Fore.RED + f"HTTP error occurred: {http_err}")
# Raise exception, print other error
except Exception as err:
    print(Fore.RED + f"Other error occurred: {err}")
# Proceed with the rest of the program
else:
    """
    Below is the JSON data which is presented:

    {
        'command_output':
            {'diff': ['list of changes between files']
            },
        'host': 'hostname'
    }

    Below we will access the usernames in the structure
    """
    diff_list = req.json()["command_output"]["diff"]
    # Check which the differences are empty, which means there are no differences in the configs
    if not diff_list:
        print(Fore.GREEN + f"No configuration differences on : {hostname}")
    else:
        print(Fore.YELLOW + f"Configuration differences on : {hostname}")
        # Iterate over list of differences, printout to screen
        for i in diff_list:
            print(Fore.YELLOW + f"Differences : {i}")
