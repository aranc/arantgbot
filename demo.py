#!/usr/bin/python
from bot import go_online, register_command

def repeat(cmd, parameters):
    return "the parameters are: <"+parameters+">"

def smile(cmd, parameters):
    return ":)"

def silent(cmd, parameters):
    print "ssshhh"

#todo: ddate/ls

register_command("repeat", repeat)
register_command("smile", smile)
register_command("silent", silent)

go_online()
