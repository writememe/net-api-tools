# Import modules
import requests
import pprint
from requests.exceptions import HTTPError
from colorama import Fore, init

# Auto-reset colorama colours back after each print statement
init(autoreset=True)

# Define variables
# Define the hostname to be queried
hostname = "lab-csr-01.lab.dfjt.local"
# Define the URL
url = "http://localhost:5000"
# Define the API path
user_host_api = "/api/nr/napalm/users/host?host="
# Define a list of allowed usernames
allowed_users = ["admin", "svc-ansible", "svc-netbox-napalm"]
# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

#Try/except block to validate a successful HTTP response code
try:
  # Get the results of the API call
  req = requests.get(url + user_host_api + hostname)
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
      print(Fore.RED + "FAILURE : The configured users are compliant")
      print(Fore.RED + "Compliant user list : " + str(allowed_users))
      print(Fore.RED +"Actual user list : " + str(configured_users))
