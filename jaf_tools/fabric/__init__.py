#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141026
"""

from termcolor import colored
from fabtools import utils

"""
Random Helper functions
"""


def display_msg(msg=None, level='info'):

    """Simple color message helper
    """

    levels = {
        'info': 'cyan',
        'warn': 'yellow',
        'error': 'red',
        'success': 'green'
    }
    if not msg:
        msg = "{}".format(colored(msg, levels[level]))

    msg = "{msg}".format(msg=colored(msg, levels[level]))
    print(msg)


def run_as_root(cmds=None):

    """
    Will run a list of commands as root
    """

    if not isinstance(cmds, list):
        display_msg('Provided your commands in a list', 'error')

    for cmd in cmds:
        utils.run_as_root(cmd)
