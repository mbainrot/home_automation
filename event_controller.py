#!/usr/bin/python

import config  # import our configuration  # noqa
import paho.mqtt.client as mqtt  # noqa
import os


def invoke_mqtt(file):
    if(os.path.exists(file) is False):
        print('ERROR - event controller - mqtt file ' + file +
              ' does not exist!')

    # Initiate connection to MQTT server in preparation to be
    # sending some messages
    with open(file, 'r') as f:
        for sLine in f.readlines():
            parts = sLine.split('|')

            if(len(parts) >= 2):
                topic = parts[0]
                body = parts[1:]

                strBody = ""
                for part in body:
                    strBody += part + "|"

                strBody = strBody.replace("\n", "")
                strBody = strBody[:-1]

                # FIXME: Put under debug switch to minimise shit in STDOUT
                # print('Got message to send to "'+topic+'" is as follows:')
                # print(strBody)
                client = mqtt.Client()
                client.connect(config.mqtt_server, 1883, 60)
                client.publish(topic, strBody)
                client.disconnect()

        f.close()


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
