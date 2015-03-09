Action definition

Directory Structure:

main.py
config.py
actions/
actions/mac/
actions/mac/info
actions/mac/dev/
actions/mac/dev/state

info = file (info about the device such as friendly name, namespace, etc)

state = file (e.g. pushed, on, off)

State file format:
line 1: action
line 2: arg0
line 3: arg1
line 4: ...

Valid actions:
forward - forwards message to another controller (i.e. its an alarm system input)
message - triggers a message (i.e. switch1 is on, turn on lightbulb1)