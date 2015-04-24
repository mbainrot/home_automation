# Home Automation
[![Build Status](https://travis-ci.org/mbainrot/home_automation.svg?branch=revert-31-update_readme)](https://travis-ci.org/mbainrot/home_automation)

Python based automation system which uses mqtt to handle intra-component communication (was formally just for use of ESP8266 devices)

## Requirements
- libcurl4-openssl-dev
- python3-pip
- python3.4
- git
- screen

## Installation
**Note:** These installation instructions are for Ubuntu 14.04

1) Install prerequisits
```
sudo -i
apt-get install mosquitto
pip install virtualenv
```
2) Setup home_automation
```
cd /
git clone https://github.com/mbainrot/home_automation.git
cd /home_automation
virtualenv env -p `which python3.4`
source env/bin/activiate
pip install -r requirements.txt
```
3) Starting home_automation
```
cd /home_automation
./start.sh
