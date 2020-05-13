# Import modules
import requests
import pprint
from requests.exceptions import HTTPError
from colorama import Fore, init

# Auto-reset colorama colours back after each print statement
init(autoreset=True)

# http://localhost:5000/api/nr/scrapli/host?host=lab-csr-01.lab.dfjt.local&command=sddhfhfhfhf

# Define variables
# Define the hostname to be queried
hostname = "lab-csr-01.lab.dfjt.local"
# Define the URL
url = "http://localhost:5000"
# Define the API path
api_path = "/api/nr/scrapli/host?host="
command_api_path = "&command="
# The command to be parsed. Use %20 for spaces
# command = "show%20archive%20config%20differences"
# The command to be parsed. Use %20 for spaces
command = "show%20archive%20config%20differences%20nvram:startup-config%20system:running-config"
# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

#Try/except block to validate a successful HTTP response code
try:
  # Get the results of the API call
  req = requests.get(url + api_path + hostname + command_api_path + command)
  # If the response was successful, no exception will be raised
  req.raise_for_status()
# Raise exception, print HTTP error
except HTTPError as http_err:
  print(Fore.RED + f'HTTP error occurred: {http_err}')
# Raise exception, print other error
except Exception as err:
  print(Fore.RED + f'Other error occurred: {err}')
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
        print(Fore.GREEN +  f'No configuration differences on : {hostname}')
    else:
        print(Fore.YELLOW + f'Configuration differences on : {hostname}')
        # Iterate over list of differences, printout to screen
        for i in diff_list:
            print(Fore.YELLOW + f"Differences : {i}")