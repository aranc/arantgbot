#!/usr/bin/python
from bot import go_online, register_command
import pexpect

def repeat(cmd, parameters):
    return "the parameters are: <"+parameters+">"

def smile(cmd, parameters):
    return ":)"

def silent(cmd, parameters):
    print "ssshhh"

def shell_word(cmd, parameters):
    return pexpect.run(cmd)

register_command("repeat", repeat)
register_command("smile", smile)
register_command("silent", silent)
register_command("ls", shell_word)
register_command("ddate", shell_word)

go_online()
