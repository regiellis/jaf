#!/usr/bin/env python
# -*- coding; utf-8 -*-

"""
jaf_tools.managers.grunt
AUTHOR: Regi E.<regi@persona.io>
CREATE/UPDATED: 20141004
"""

import os
import subprocess

from termcolor import colored
from flask.ext.script import Manager, prompt_bool



manager = Manager(usage="Grunt Management Tasks")

# DIR CONFIGS - TODO: Find a better way
# NOTE CWD IS BASED ON WHERE THE MANAGEMENT SCRIPT
# IS EXECUTED. AS THIS IS A SUBMANAGER, EXECUTION
# WILL HAPPEN AT THE "manage.py" level
GRUNT_CWD = os.path.abspath('jaf_tools/frontend/')


# SUBPROCESS HELPER
def grunt_cmd(grunt_cmd=None):

    """ SUBPROCESS HELPER """
    if not grunt_cmd and not isinstance(grunt_cmd, str):
        print "Need to provide command as a string"

    os.chdir(GRUNT_CWD)
    response = subprocess.call([grunt_cmd], shell=True)

    return response


@manager.command
def santy_check():

    """
    Runs a santy check via jshint on the Gruntfile
    """
    grunt_cmd("grunt jshint")
    return None


@manager.command
def screenshot():

    """
    Will start a application instance and take screenshots
    of the resolutions at options defined in the Gruntfile
    """

    grunt_cmd("grunt screenshot")
    return None


@manager.command
def rebuild():

    """
    Will rebuild all project assets files under
    the development flag
    """

    grunt_cmd("grunt rebuild")
    return None


@manager.command
def build():

    """
    Will build all project assets files under
    the production flag
    """

    grunt_cmd("grunt build")
    return None


@manager.command
def clean():

    """
    Will remove all generated project assets
    """

    answer = prompt_bool(colored("Are you sure you want to delete you assets?", 'red'))
    if answer:
        grunt_cmd("grunt clean")
        print "{msg}".format(msg=colored("Your assets have been cleaned", 'green'))
        return None
    print "{msg}".format(msg=colored("Nothing was removed", 'green'))
    return None
