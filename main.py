#!/usr/bin/python

# Import our configuration
import config  # import our configuration
import event_controller  # import our event controller
import lifx_controller  # import our LIFX Controller

# Import external modules
import paho.mqtt.client as mqtt
import subprocess
import threading
import os
import time
import datetime


def handle_sys(client, msg):
    parts = msg.split("|")
    # Payload: sender_mac,dest_mac,device_id,device_state

    if(len(parts) == 2):
        command, arg0 = parts

        if(command == "!register"):
            dev_mac = arg0

            client.subscribe("sys_" + arg0)

            # FIXME
            print("I am meant to record the devices registration here!")
            # FIXME

            client.publish("sys_" + dev_mac, "!registered")
            client.publish("sys_" + dev_mac, "!ping|1234")


def handle_device_input(client, msg, smsg):
    parts = smsg.split("|")

    target_mac = str(msg.topic).replace("input_", "")


def handle_device_output(client, msg, smsg):
    parts = smsg.split("|")

    target_mac = str(msg.topic).replace("output_", "")


def handle_device_sys(client, msg, smsg):
    parts = smsg.split("|")

    target_mac = str(msg.topic).replace("sys_", "")

    if(smsg.startswith("!pong")):
        touch_arg = config.working_dir + "/devices/" + target_mac

        res = subprocess.call(["touch", touch_arg])


def createdir_ifnot_exist(dir):
    if(os.path.exists(dir) is False):
        os.mkdir(dir)


def check_and_fix_crontab_dirs():
    createdir_ifnot_exist(config.working_dir + "/events/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/sunday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/monday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/tuesday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/wednesday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/thursday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/friday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/saturday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/everyday/")
    createdir_ifnot_exist(config.working_dir + "/events/crontab/everycron/")


def trigger_directory(dir):
    strVoid = ""  # FIXME


def handle_crontab(client, msg, smsg):
    # This simply
    check_and_fix_crontab_dirs()
    sVoid = ""
    now = datetime.datetime.now()

    strHour = str(now.hour)
    strMinute = str(now.minute)
    strDow = now.strftime("%a").lower()

    if(now.hour < 10):
        strHour = '0' + strHour

    if(now.minute < 10):
        strMinute = '0' + strMinute

    currentTimePath_a = config.working_dir +
    "/events/crontab/everyday/" + strHour + strMinute + "/"

    currentTimePath_b = config.working_dir +
    "/events/crontab/" + strDow + "/" + strHour + strMinute + "/"

    everycron = config.working_dir + "/events/crontab/everycron/"

    if(os.path.exists(currentTimePath_a)):
        event_controller.process_event_folder(currentTimePath_a)

    if(os.path.exists(currentTimePath_b)):
        event_controller.process_event_folder(currentTimePath_b)

    event_controller.process_event_folder(everycron)


def timer_poll_devices():
    # do something here ...
    print("Polling all \"active\" devices!")

    dev_path = config.working_dir + "/devices/"

    for dirname, dirs, files in os.walk(dev_path):
        for sfile in files:
            (mode, ino, dev, nlink, uid, gid, size, atime,
                mtime, ctime) = os.stat(dev_path + sfile)

            timediff = time.time() - mtime

            if(timediff < config.dev_timeout):
                print(sfile + " " + str(timediff))

                client.publish("sys_" + sfile, "!ping|1234")
            else:
                os.remove(dev_path + sfile)

    threading.Timer(10, timer_poll_devices).start()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Input channels (device -> server)
    client.subscribe("input")  # Generic input channel
    client.subscribe("input_ack")  # ack input channel
    client.subscribe("input_admin")  # Administrative input channel

    # System Channels (any <> any)
    client.subscribe("sys")  # Generic system channel
    client.subscribe("sys_hbeat")  # Heartbeat channel
    client.subscribe("sys_ack")  # Ack channel (not applicable to server)

    # Output channels (server -> device)
    client.subscribe("output")  # Generic output channel
    client.subscribe("output_ack")  # ack output channel
    client.subscribe("output_admin")  # admin output channel???

    # Crontab
    client.subscribe("crontab")

    # Lifx
    client.subscribe("lifx")

    threading.Timer(10, timer_poll_devices).start()

    client.publish("sys", "!reregister")


def on_message(client, userdata, msg):
    newStr = str(msg.payload)
    # newStr = newStr.replace("b'","")
    newStr = newStr[2:-1]

    print("recv: topic=" + msg.topic + " payload=" + newStr)

    if(msg.topic == "input"):  # generic input
        sVoid = ""  # FIXME
    elif(msg.topic == "input_ack"):  # Input req ACK
        sVoid = ""  # FIXME
    elif(msg.topic == "input_admin"):  # Administrative input
        sVoid = ""  # FIXME
    elif(msg.topic == "sys"):  # Generic system
        handle_sys(client, newStr)
    elif(msg.topic == "sys_hbeat"):  # System heartbeats (both client & server)
        sVoid = ""  # FIXME
    elif(msg.topic == "sys_ack"):  # System ack channel (n/a to server)
        sVoid = ""  # FIXME
    elif(str(msg.topic).startswith("sys_")):  # Device specific sys channel
        handle_device_sys(client, msg, newStr)
    elif(str(msg.topic) == "crontab"):
        handle_crontab(client, msg, newStr)
    elif(str(msg.topic) == "lifx"):
        lifx_controller.handle_lifx_message(client, msg, newStr)
    else:  # Message we don't recognise...
        sVoid = ""  # FIXEME

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.mqtt_server, 1883, 60)

client.loop_forever()
