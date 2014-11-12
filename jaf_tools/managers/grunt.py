#!/usr/bin/env python
# -*- coding; utf-8 -*-

"""
jaf_tools.managers.grunt
AUTHOR: Regi E.<regi@persona.io>
CREATE/UPDATED: 20141004
"""

import os
import subprocess32

from termcolor import colored
from flask.ext.script import Manager, prompt_bool



manager = Manager(usage="Grunt Management Tasks")

# DIR CONFIGS - TODO: Find a better way
# NOTE CWD IS BASED ON WHERE THE MANAGEMENT SCRIPT
# IS EXECUTED. AS THIS IS A SUBMANAGER, EXECUTION
# WILL HAPPEN AT THE "manage.py" level
GRUNT_CWD = os.path.abspath('jaf_tools/frontend/')


# SUBPROCESS HELPER
def grunt_cmd(grunt_cmd=None, msg=None):

    """ SUBPROCESS HELPER """
    if not grunt_cmd and not isinstance(grunt_cmd, str):
        print "{msg}".format(msg=colored("Need to provide command as a string", 'red'))

    os.chdir(GRUNT_CWD)
    response = subprocess32.call([grunt_cmd], shell=True)
    print "{msg}".format(msg=colored(msg, 'green'))

    return response


def install_grunt():

    """
    Installs grunt, grunt-cli and alias the command
    locally
    """

    os.chdir(GRUNT_CWD)
    response = subprocess32.call(['npm install', 'npm link grunt-cli'], shell=True)
    return response


def install_bower():

    """
    Installs grunt, grunt-cli and alias the command
    locally
    """

    os.chdir(GRUNT_CWD)
    response = subprocess32.call(['bower install', 'grunt bower'], shell=True)
    return response


@manager.command
def install_all_packages_and_assets():

    """
    Installs all needed packages and assets for
    the applications
    """
    install_grunt()
    install_bower()
    return None


@manager.command
def santy_check():

    """
    Runs a santy check via jshint on the Gruntfile
    """

    grunt_cmd("grunt jshint")
    return None


@manager.command
def develop():

    """
    Starts a application instance with browsersync for
    development
    """
    grunt_cmd("grunt develop", "Development Server Running")
    return None


@manager.command
def screenshot():

    """
    Starts a application instance and take screenshots
    of the resolutions at options defined in the Gruntfile
    """

    grunt_cmd("grunt screenshot", "All screenshots have been taken")
    return None


@manager.command
def rebuild():

    """
    Rebuilds all project assets files under
    the development flag
    """

    grunt_cmd("grunt rebuild", "Project has been rebuilt")
    return None


@manager.command
def build():

    """
    Builds all project assets files under
    the production flag
    """

    grunt_cmd("grunt build", "Project has been built for deployment")
    return None


@manager.command
def clean():

    """
    Removes all generated project assets
    """

    answer = prompt_bool(colored("Are you sure you want to delete you assets?", 'red'))
    if answer:
        grunt_cmd("grunt clean", msg="Your assets have been cleaned")
        return None
    print "{msg}".format(msg=colored("Nothing was removed", 'green'))
    return None
