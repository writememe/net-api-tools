# Import modules
import requests
import pprint


# Define variables
# Define the hostname to be queried
hostname = "lab-csr-01.lab.dfjt.local"
# Define the URL
url = "http://localhost:5000"
# Define the API path
user_host_api = "/api/nr/users/host?host="
# Define a list of allowed usernames
allowed_users = ["admin", "svc-ansible", "svc-netbox-napalm"]

# Set indentation on pretty prinr
pp = pprint.PrettyPrinter(indent=2)


# Get the results of the API call and extract the JSON response
req = requests.get(url + user_host_api + hostname).json()
# Debug pretty print
# pp.pprint(req)


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
# Access the username level of the dictionary
user_list = req[hostname]["users"]
# Debug pretty print
# pp.pprint(user_list)
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
    print("SUCCESS : The configured users are compliant")
    print("Compliant user list : " + str(allowed_users))
    print("Actual user list : " + str(configured_users))
else:
    print("FAILURE : The configured users are compliant")
    print("Compliant user list : " + str(allowed_users))
    print("Actual user list : " + str(configured_users))
