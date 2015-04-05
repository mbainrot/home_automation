#!/usr/bin/python

import config  # import our configuration
import paho.mqtt.client as mqtt
import os


def invoke_mqtt(file):
    strVoid = ""  # FIXME: BLOCKER


def invoke_py(file):
    if(os.path.exists(file)):
        os.system("/usr/bin/python " + file)


def invoke_cmd(file):
    if(os.path.exists(file)):
        os.system("/bin/bash " + file)


def process_event_folder(path):
    # Process a folder when the event fires

    for dirname, dirs, files in os.walk(path):
        for file in files:
            process_event_file(path + "/" + file)


def process_event_file(path):
    # Process each event file
    if(path.endswith(".mqtt")):
        invoke_mqtt(path)
    elif(path.endswith(".py")):
        invoke_py(path)
    elif(path.endswith(".cmd")):
        invoke_cmd(path)
