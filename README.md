![net-api-tools](https://github.com/writememe/net-api-tools/workflows/net-api-tools/badge.svg?branch=master)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# Introduction

This repository contains a reference set of tools and solutions which leverage the [`net-api`](https://github.com/writememe/net-api) platform.  

These tools have been developed with the intent to show how simple and flexible it is to consume `net-api` and write custom applications for your business needs.  

Whilst these solutions are written in Python, there is nothing preventing you from consuming `net-api` using any other language of your choice.


## Structure

All examples are contained within the [examples/](examples/) directory. Below is a reference table detailing the high level examples:

| Subject | Description | File |
| ------- | --------------- | ---------------- |
| Local username compliance | Validate that the local usernames defined on a host exactly match a pre-defined list | [local-username-compliance.py](examples/local-username-compliance.py)|
| Running config versus startup config report | Validate that there are no differences between the running and startup config on an IOS host |[ios-config-diff-report.py](examples/ios-config-diff-report.py) |
| All host NTP server compliance | Validate that all NTP servers defined on all hosts exactly match a pre-defined list |[all-ntp-servers.py](examples/all-ntp-servers.py) |

**NOTE: All the examples provided are supported using Python 3.6 or higher**

## Contributing

I will try to populate more examples as time dictates, however if you would like to contribute, that would be great!  

The more examples and use cases that are generated, the more useful the tool is for others throughout the community. 

If you need some help on how or where to start, please let me know. Thanks
