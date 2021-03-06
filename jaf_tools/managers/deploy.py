#!/usr/bin/env python
# -*- coding; utf-8 -*-

"""
jaf_tools.managers.deploy
AUTHOR: Regi E.<regi@persona.io>
CREATE/UPDATED: 20141004
"""

import os
import subprocess32

from termcolor import colored
from flask.ext.script import Manager, prompt_bool

manager = Manager(usage="Deployment Options")

# DIR CONFIGS - TODO: Find a better way
# NOTE CWD IS BASED ON WHERE THE MANAGEMENT SCRIPT
# IS EXECUTED. AS THIS IS A SUBMANAGER, EXECUTION
# WILL HAPPEN AT THE "manage.py" level
CWD = os.path.abspath('jaf_tools/templates/')


@manager.command
def nginx_template():

    """
    Creates template for deploying on nginx
    """

    pass


@manager.command
def heroku_template():

    """
    Creates a template for deploying on heroku
    """

    pass


@manager.command
def create_uwsgi_file():

    """
    Creates the projects uWSGI file for Deployment
    """

    pass
