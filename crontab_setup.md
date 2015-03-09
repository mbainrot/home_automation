How to setup crontab
Set up a crontab event under any user (atleast any user that has access to kick mosquitto in the face) as follows


* * * * *     mosquitto_pub -t crontab -m ""

This will cause the automation server to automatically create the directory structure under events/crontab/ as follows
crontab
crontab\everything (evaluates all events regardless of time)
crontab\everyday (evaluates events under each time folder (does not create time folder) hhmm/)
crontab\sunday
crontab\monday
crontab\tuesday
crontab\wednesday
crontab\thursday
crontab\friday
crontab\saturday

Under all the crontab subfolders EXCEPT everything, it looks for a subfolder called "hhmm" then if it exists looks for subfiles