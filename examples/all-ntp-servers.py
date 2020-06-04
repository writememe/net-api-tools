"""
This application will validate all NTP servers on all hosts defined
on `net-api` against a pre-defined list and print successes and/or
failures.

To adjust this to your environment, please change the `url` variable
and the `allowed_ntp_servers` variable within the code.

To execute this code, please run the following command:

python all-ntp-servers.py --help

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
    description="Collect all NTP servers configured on all hosts."
)
# Add debug argument, set to False by default unless required
parser.add_argument(
    "--debug",
    action="store_true",
    help="Provide additional debugging output. True for debugging, set to False by default",
)
args = parser.parse_args()

print(Fore.CYAN + "Collecting NTP servers, please wait ...")
# Define the URL
url = "http://10.0.0.54:5000"
# Define the API path
api_path = "/api/v1/nr/napalm/ntp_servers/all"
# Define a list of allowed NTP servers
allowed_ntp_servers = ["10.0.0.1", "8.8.8.8"]
# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

# Try/except block to validate a successful HTTP response code
try:
    # If debug is set to True, provide the full API call string
    if args.debug is True:
        print(Fore.MAGENTA + f"Attempting API call - {url}{api_path}")
    # Get the results of the API call
    req = requests.get(url + api_path)
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

  { 'hostname-1.lab.acme.local': { 'ntp_servers': { '8.8.4.4': {},
                                                  '4.2.2.2': {},
                                                  '8.8.8.8': {}}},
    'hostname-2.lab.acme.local': { 'ntp_servers': { '8.8.4.4 prefer': {},
                                                      '8.8.8.8': {}}},
    'hostname-3.lab.acme.local': { 'ntp_servers': { '8.8.4.4': {},
                                                      '8.8.8.8': {}}},
    'hostname-4.lab.acme.local': {'ntp_servers': {'8.8.4.4': {}, '8.8.8.8': {}}},
    'hostname-5.lab.acme.local': { 'ntp_servers': { '8.8.4.4': {},
                                                      '8.8.8.8': {}}},
    'hostname-6.lab.acme.local': { 'ntp_servers': { '8.8.4.4': {},
                                                    '8.8.8.8': {}}}}
    Below we will access the NTP servers in the structure
  """
    # Extract the JSON response
    ntp_results = req.json()
    # Iterate through NTP servers, using the host as the iterator
    for host in ntp_results.keys():
        # print(Fore.GREEN + f"Hostname - {host}")
        # Assign NTP Server results inside the original JSON response to a variable
        ntp_servers = ntp_results[host]["ntp_servers"]
        # Create an empty list to append configured NTP servers into
        configured_ntp_servers = list()
        # For loop to iterate over NTP server results
        for server in ntp_servers.keys():
            # Append to the list and right strip the " prefer" off entries such as "10.0.0.1 prefer"
            configured_ntp_servers.append(server.rstrip(" prefer"))
        # Sort both lists, for comparison
        allowed_ntp_servers.sort()
        configured_ntp_servers.sort()
        # If/else list comparision to check that allowed
        # NTP servers exactly match what is on the device.
        if configured_ntp_servers == allowed_ntp_servers:
            print(
                Fore.GREEN
                + f"SUCCESS : The configured NTP servers are compliant on {host}"
            )
            print(
                Fore.GREEN + "Compliant NTP server list : " + str(allowed_ntp_servers)
            )
            print(
                Fore.GREEN + "Actual NTP server list : " + str(configured_ntp_servers)
            )
        else:
            print(
                Fore.RED
                + f"FAILURE : The configured NTP servers are NOT compliant on {host}"
            )
            print(Fore.RED + "Compliant server list : " + str(allowed_ntp_servers))
            print(Fore.RED + "Actual server list : " + str(configured_ntp_servers))
        # Demarcation print
        print("=" * 80)
