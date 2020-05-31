"""
This application will validate all users on an individual Nornir
host defined on `net-api` against a pre-defined list and print
successes and/or failures.

To adjust this to your environment, please change the `url` variable
and the `allowed_users` variable within the code.

To execute this code, please run the following command:

python local-username-compliance.py --help

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
    description="Validate local username(s) compliance on given host."
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

print(Fore.CYAN + f"Validating local usernames on {args.host}")
# Take argparse input and assign to the hostname variable
hostname = args.host
# Define the URL
url = "http://10.0.0.54:5000"
# Define the API path
api_path = "/api/v1/nr/napalm/users/host?host="
# Define a list of allowed usernames
allowed_users = ["admin", "svc-ansible", "svc-netbox-napalm"]
# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

# Try/except block to validate a successful HTTP response code
try:
    # If debug is set to True, provide the full API call string
    if args.debug is True:
        print(Fore.MAGENTA + f"Attempting API call - {url}{api_path}{hostname}")
    # Get the results of the API call
    req = requests.get(url + api_path + hostname)
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
    "hostname": {
      "users": {
        "username1": {
          "level": 15,
          "password": "$1$Xa0G$mSJ/Cp70.lRDgcn.SXL1r.",
          "sshkeys": []
        },
        "username2": {
          "level": 15,
          "password": "$1$oiur$guHYCob2ovmb5AB5ugDYw/",
          "sshkeys": []
        },
        "username3": {
          "level": 15,
          "password": "$1$Ln6l$1oPnApd2BSXchOQI3ifbd1",
          "sshkeys": []
        }
      }
    }
  }

  Below we will access the usernames in the structure
  """
    # Extract the JSON response and access the username level of the dictionary
    user_list = req.json()[hostname]["users"]
    # Create an empty list, for the username(s) on the device to be entered into
    configured_users = list()
    # Iterate over the keys in the list, which are the username(s)
    for key in user_list.keys():
        # Append the list with the username entries
        configured_users.append(key)
    # Sort both lists, for comparison
    allowed_users.sort()
    configured_users.sort()
    # If/else list comparision to check that allowed
    # usernames exactly match what is on the device.
    if configured_users == allowed_users:
        print(Fore.GREEN + "SUCCESS : The configured users are compliant")
        print(Fore.GREEN + "Compliant user list : " + str(allowed_users))
        print(Fore.GREEN + "Actual user list : " + str(configured_users))
    else:
        print(Fore.RED + "FAILURE : The configured users are NOT compliant")
        print(Fore.RED + "Compliant user list : " + str(allowed_users))
        print(Fore.RED + "Actual user list : " + str(configured_users))
