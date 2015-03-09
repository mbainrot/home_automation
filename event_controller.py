#!/usr/bin/python

import config # import our configuration
import paho.mqtt.client as mqtt
import os

def invoke_mqtt(file):
	strVoid = ""

def invoke_py(file):
	if(os.path.exists(file):
		os.system("/usr/bin/python " + file) # its dirty, its nasty, but its oh so delicious

def invoke_cmd(file):
	if(os.path.exists(file):
		os.system("/bin/bash " + file) # its dirty, its nasty, but its oh so delicious

def process_event_folder(path):
	# Process a folder when the event fires
	
	for dirname,dirs,files in os.walk(path):
		for file in files:
			process_event_file(path + "/" + file)

def process_event_file(path):
	# Process each event file
	if(path.endswith(".mqtt")):
		strVoid = "" # Handle MQTT file
	elif(path.endswith(".py")):
		strVoid = "" # Handle MQTT file
	elif(path.endswith(".sh")):
		strVoid = "" # Handle MQTT file