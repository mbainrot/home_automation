#!/usr/bin/python

# ###########################################################################
# LIFX API CONTROLLER
# AUTHOR: MAX BAINROT
# DESC: Implements LIFX control via their Cloud API
# ###########################################################################


import config # import our configuration
import lifx_config # import lifx config
import paho.mqtt.client as mqtt
import os

# Interfacing with LIFX additional improts......
import pycurl
from io import BytesIO

def _lifx_json_get(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, lifx_config.lifx_apiserver + url)
    c.setopt(c.HTTPHEADER,['Authorization: Bearer ' + lifx_config.lifx_apikey])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('iso-8859-1')

    return body

def _lifx_json_put(url,data):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, lifx_config.lifx_apiserver + url)
    c.setopt(c.HTTPHEADER,['Authorization: Bearer ' + lifx_config.lifx_apikey])
    c.setopt(c.CUSTOMREQUEST, 'PUT')
    c.setopt(c.POSTFIELDS, data)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('iso-8859-1')

    return body

def handle_lifx_message(client,msg,smsg):
    # client = mqtt client
    # msg = msg object
    # smsg = string of content

    parts = smsg.split("|")

    if(len(parts) < 1):
        return

    cmd = parts[0]

    # parts == 2
    if(len(parts) == 2):

        if(cmd == "!turn_on"): # !turn_on,light_id
            light_id = parts[1]
            print(_lifx_json_put("/lights/id:" +light_id + "/power","state=on"))


        if(cmd == "!turn_off"): # !turn_off,light_id
            light_id = parts[1]
