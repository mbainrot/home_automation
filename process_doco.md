Ongoing:
- Every 30 seconds, send UDP broadcast on port 12345 disclosing IP of ha server

Registration:
- Device subscribes to sys
- Device subscribes to sys_<device mac>
- Device sends message to sys "!register|<mac>"
- Server registers to sys_<device mac>
- Server responds via sys_<device mac> "!registered"
- Server pings device
- Device responds, server touches <script directory>/devices/<device mac>

Post registration:
- Device subscribes to input_<mac> and output_<mac>

Event happening (button push)
- Device polls event on input_<mac> (e.g. !event,switch1,on)
- Server looks it up and works out what to do (e.g output_<mac of lightbulb>,!on light0)