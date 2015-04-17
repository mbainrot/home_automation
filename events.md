Events are supported and defined via file extensions

somefilename.mqtt
This is an mqtt command file, it is formatted topic|message

Subsequent "|" are perfectly acceptable because the event_controller is inteligent enough to automatically pay attention to the topic and forward the rest

somefilename.sh
This is a bash command (shell file), it does not need to have +x set in order for the command to take effect

somefilename.py
This is a python file, like the bash command it also does not need +x in order to function.

Events enable the chaining and grouping of commands for example, say we had a serries of light globes to be turned on when *DE:AD:BE:EF:FE:ED* *switch1* was *pressed* we would do the following

events/DE:AD:BE:EF:FE:ED/switch1/pressed/someMeaningfulFilename.mqtt:
'''
custom|turn_on_all_lights
'''

This will trigger an input event, to fire the custom event "turn_on_all_lights"

Inside of events/custom/turn_on_all_lights/somefilename.mqtt we'd have
'''
lifx|!turn_on|abc0001
lifx|!turn_on|abc0002
lifx|!turn_on|abc0003
'''

So when *DE:AD:BE:EF:FE:ED*'s *switch1* is *pressed*, it will fire a mqtt message to *input*, which would tell it to process *custom* event *turn_on_all_lights*

This in turn would fire the turn_on_all_lights script and because we have not specified a sub event it evaluates all files inside of the folder

This would then go through the file and fire off commands to the lifx module, instructing the bulbs to turn on.


This functionality is very powerful and as a result great power comes with great responsibility. It is very plausable (and easy in actual fact) to accidentially cause a race condition and crash the server :P

Though with thorough planing this should not be an issue.
