#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools.fabric.database_setup
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141110
"""

import os
import subprocess32

from string import Template
from fabric.api import *
from fabric.operations import run
from fabtools.deb import install

# Module imports
from . import run_as_root, display_msg


def setup_database(env, **kwargs):
    """Install and configure rethinkdb on the ubuntu server
    """
    display_msg('Creating database store for project...')
    # Install rethinkdb from source
    source = ['source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list',
              'wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -']
    run_as_root(source)
    install('rethinkdb', update=True)
    display_msg('Database setup complete...', 'success')
    config_database(env)


def config_database(env, **kwargs):
    """Do initial configration on database server
    """
    display_msg('Configure database')

    with lcd(env.template_dir):
        with open('database', 'r') as database_config:
            print database_config.read()

    #put(os.path.join(env.template_dir, 'database'), '/tmp/database')


def flush_database():
    pass


def restart_datbase():
    pass


def stop_database():
    pass


