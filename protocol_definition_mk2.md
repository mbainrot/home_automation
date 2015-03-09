topic:
broadcast - topic that all devices/controllers listen to
controller - topic that only controllers listen to
device_<device mac/id> - topic that the device listens to

messages:

basic message format:
<cmd>,<target>,<source>,etc

All messages must contain the first three elements to be processed, mqtt cannot allow specific targeting so lack of information means the device cannot workout who it's meant to go to (or who the heck sent it)

target & source info is either mac address or alias, mac addresses will ALWAYS work, i.e. you can always reach the master either by it's alias or it's mac address

!command - issued by the controller to the children to do something
!command,<target>,<source>,<cmd>,<arg0>,<arg1>,...

!command_ack - issued by the controller to the children and requires an ack
!command_ack,<target>,<source>,<unique_id>,<cmd>,<arg0>,<arg1>,...

!ack - Acknowledgement of a message requiring an ACK
!ack,<target>,<source>,<unique_id>,<msg being ack'd>

!event - issued by a client to the/a controller
!event,<target>,<source>,<arg0>,<arg1>,...

!heartbeat - used by a device/controller to acknowledge it's existance
!heartbeat,<target>,<source>,<unique_id>

!register - command to register the device?