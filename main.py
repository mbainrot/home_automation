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
# import io
import time
import datetime

bRemoteKill = False
bStop = False
PollTimer = None


def handle_sys(client, msg):
    parts = msg.split("|")
    # Payload: sender_mac,dest_mac,device_id,device_state

    if(len(parts) == 2):
        command, arg0 = parts

        if(command == "!register"):
            dev_mac = arg0

            client.subscribe("input_" + dev_mac)
            client.subscribe("sys_" + dev_mac)

            # FIXME: These are debugs!
            client.subscribe("output_" + dev_mac)

            # Respond to the client's registeration
            client.publish("sys_" + dev_mac, "!registered")
            client.publish("sys_" + dev_mac, "!send_caps")
            client.publish("sys_" + dev_mac, "!ping|1234")

        if(command == "!unittest"):
            client.publish("sys_ack", "!hello")


def handle_input(client, msg, smsg):  # FIXME
    parts = smsg.split("|")  # noqa

    if(len(parts) != 4):
        return

    sender_mac = parts[0]
    # dest_mac = parts[1]
    component = parts[2]
    event = parts[3]

    tempPath = config.working_dir + "/events/" + sender_mac + "/" + \
        component + "/" + event

    if(os.path.exists(tempPath)):
        event_controller.process_event_folder(tempPath)


def handle_targeted_input(client, msg, smsg):  # FIXME
    parts = smsg.split("|")  # noqa

    sender_mac = msg.topic.replace("input_", "")

    if(len(parts) != 2):
        return

    component = parts[0]
    event = parts[1]

    tempPath = config.working_dir + "/events/" + sender_mac + "/" + \
        component + "/" + event

    if(os.path.exists(tempPath)):
        event_controller.process_event_folder(tempPath)


def handle_device_output(client, msg, smsg):  # FIXME
    parts = smsg.split("|")  # noqa

    target_mac = str(msg.topic).replace("output_", "")  # noqa


def handle_device_sys(client, msg, smsg):  # FIXME
    parts = smsg.split("|")  # noqa

    target_mac = str(msg.topic).replace("sys_", "")

    if(smsg.startswith("!pong")):
        touch_arg = config.working_dir + "/devices/" + target_mac

        subprocess.call(["touch", touch_arg])

    if(smsg.startswith("!capability") and len(parts) == 3):
        component = parts[1]
        event = parts[2]

        basedir = config.working_dir + "/events/" + target_mac.upper()

        createdir_ifnot_exist(basedir)
        createdir_ifnot_exist(basedir + "/" + component)
        createdir_ifnot_exist(basedir + "/" + component + "/" + event)


def createdir_ifnot_exist(dir):
    if(os.path.exists(dir) is False):
        os.mkdir(dir)


def createfile_ifnot_exist(file):
    if(os.path.exists(file) is False):
        touch_file(file)


def touch_file(sFile):
    f = open(sFile, 'w')
    f.write("")
    f.close()


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


def check_and_fix_event_dirs():
    createdir_ifnot_exist(config.working_dir + "/events/")
    createdir_ifnot_exist(config.working_dir + "/events/custom/")


def handle_crontab(client, msg, smsg):
    # Setup our directories
    check_and_fix_crontab_dirs()

    now = datetime.datetime.now()

    strHour = str(now.hour)
    strMinute = str(now.minute)
    aDaysOfTheWeek = ("sunday", "monday", "tuesday", "wednesday",
                      "thursday", "friday")
    strDow = aDaysOfTheWeek[int(now.strftime("%w"))]

    if(now.hour < 10):
        strHour = '0' + strHour

    if(now.minute < 10):
        strMinute = '0' + strMinute

    currentTimePath_a = config.working_dir + \
        "/events/crontab/everyday/" + strHour + strMinute + "/"

    currentTimePath_b = config.working_dir + \
        "/events/crontab/" + strDow + "/" + strHour + strMinute + "/"

    print("Current Day of the week is: " + strDow)  # FIXME: RM_DEBUG

    everycron = config.working_dir + "/events/crontab/everycron/"

    if(os.path.exists(currentTimePath_a)):
        event_controller.process_event_folder(currentTimePath_a)

    if(os.path.exists(currentTimePath_b)):
        event_controller.process_event_folder(currentTimePath_b)

    event_controller.process_event_folder(everycron)


def timer_poll_devices(client):
    if(client.bStop is True):
        print("Stopping the timer_poll_devices timer!")
        return

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

    threading.Timer(10, timer_poll_devices, (client,)).start()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Input channels (device -> server)
    client.subscribe("input")  # Generic input channel

    # System Channels (any <> any)
    client.subscribe("sys")  # Generic system channel
    client.subscribe("sys_hbeat")  # Heartbeat channel
    client.subscribe("sys_ack")  # Ack channel (not applicable to server)

    # Output channels (server -> device)
    client.subscribe("output")  # Generic output channel

    # Custom
    client.subscribe("custom")

    # Crontab
    client.subscribe("crontab")

    # Remote kill (used for unittesting)
    if client.bRemoteKill is True:
        client.subscribe("abort")

    # Lifx
    client.subscribe("lifx")

    threading.Timer(10, timer_poll_devices, (client,)).start()

    client.publish("sys", "!reregister")


def handle_custom(client, msg, smsg):
    tempPath = config.working_dir + "/events/custom/" + smsg

    if(os.path.exists(tempPath) is False):
        return

    event_controller.process_event_folder(tempPath)


def on_message(client, userdata, msg):
    newStr = msg.payload.decode(encoding='ascii')

    print("recv: topic=" + msg.topic + " payload=" + newStr)

    if(msg.topic == "input"):  # generic input
        handle_input(client, msg, newStr)
    elif(msg.topic == "sys"):  # Generic system
        handle_sys(client, newStr)
    elif(msg.topic == "sys_hbeat"):  # System heartbeats (both client & server)
        raise NotImplementedError()  # FIXME
    # elif(msg.topic == "sys_ack"):  # System ack channel (n/a to server)
    #    raise NotImplementedError()  # FIXME
    elif(str(msg.topic).startswith("sys_")):  # Device specific sys channel
        handle_device_sys(client, msg, newStr)
    elif(str(msg.topic).startswith("input_")):
        handle_targeted_input(client, msg, newStr)
    elif(str(msg.topic) == "custom"):
        handle_custom(client, msg, newStr)
    elif(str(msg.topic) == "crontab"):
        handle_crontab(client, msg, newStr)
    elif(str(msg.topic) == "lifx"):
        lifx_controller.handle_lifx_message(client, msg, newStr)
    elif(str(msg.topic) == "abort"):
        print("RECEIVED KILL MESSAGE, DYING")
        client.bStop = True
        client.disconnect()
    else:  # Message we don't recognise...
        strVoid = ""  # noqa


def main(bRemoteKill):
    check_and_fix_event_dirs()
    check_and_fix_crontab_dirs()

    client = mqtt.Client()
    client.bRemoteKill = bRemoteKill
    client.bStop = False

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.mqtt_server, 1883, 60)

    while client.bStop is False:
        client.loop()

    print("Main loop stopped!")


def fork_main():
    t = threading.Thread(target=main, daemon=True, args=(True,))
    t.start()
    return t


if __name__ == '__main__':
    main(True)
