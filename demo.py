#!/usr/bin/env python3
import sys
import time
import os
import pexpect
from bot import go_online, register_command

def repeat(cmd, parameters):
    return "the parameters are: <"+parameters+">"

def smile(cmd, parameters):
    return ":)"

def silent(cmd, parameters):
    print "ssshhh"

def shell_word(cmd, parameters):
    return pexpect.run(cmd)

def spam(cmd, parameters):
    newpid = os.fork()
    if newpid != 0: return
    print "spawning spam"
    cmd = "~/arantgbot/spam_demo.py " + str(parameters)
    p = pexpect.spawn('bash -c "'+cmd+'"', logfile=sys.stdout)
    p.interact()
    print "spam spinning stopped"
    sys.exit()

register_command("repeat", repeat)
register_command("smile", smile)
register_command("silent", silent)
register_command("ls", shell_word)
register_command("ddate", shell_word)
register_command("spam", spam)

go_online()
