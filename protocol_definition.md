# Protocol Definition #

All payloads will start with
sender_mac,dest_mac, ...

dest_mac is either destination device or 
broadcast: FF:FF:FF:FF:FF:FF
controller: 00:00:00:00:00:00
alarm controller: 00:00:00:00:00:01


generic input - unreliable, does not expect acknowledge and sends once
Topic: input or output
Payload: sender_mac,dest_mac,device_id,device_state

generic ack input, reliable-ish, will continue sending message until acknowledged
Topic: input_ack or output_ack
Payload: sender_mac,dest_mac,msg_id,device_id,device_state

device -> server heartbeat (nb, expects ack)
topic: sys_hbeat
payload: sender_mac,00:00:00:00:00:00,msg_id

ack response (server -> child device)
Topic: sys_ack
Payload: 00:00:00:00:00:00,dest_mac,msg_id,ack_status,device_id,device_state

ack_status =
ack = acknowledged and processed successfully
nack = acknowledged, but errored (aka, "yeah I heard you, I ain't doin anything, now please shut up now...")

server broadcast heartbeat (not ack'd)
topic: sys_hbeat
payload: 00:00:00:00:00:00,FF:FF:FF:FF:FF:FF,server_ok


Examples:

Toggle switch going from off to on position

DEVICE
topic: input_ack
payload: 64:27:37:30:ba:c4|00:00:00:00:00:00|msg0001|switch1|on

CONTROLLER acknowledgement
topic: sys_ack
payload: 00:00:00:00:00:00|64:27:37:30:ba:c4|msg0001|ack|switch1|on