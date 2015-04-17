# Protocol Definition #

## Device Registration ##
When a device first fires up it registers itself with the server.

This is done by:
client -> server (sys): !register|mac
Server then subscribes to the sys_~mac~ channel
server -> client (sys_~mac~): !registered
server -> client (sys_~mac~): !send_caps
server -> client (sys_~mac~): !ping|1234
client -> server (sys_~mac~): !pong|1234

If the device is an input device (e.g. sensor/light switch) it will respond to !send_caps with
client -> server (sys_~mac~): !capability|component|event

This will cause the server to automatically populate events/~mac~/component/event/ if they do not exist

When the server starts up it sends out a command to !reregister which causes all child devices to !register, this is so that after a state loss it can recover

## Input Devices ##
When an input device endures an event it will send the following
client -> server (input_~mac~): component|event

At this point in time I have not implemented acknowledged events so the message could get missed
