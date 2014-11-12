#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools.fabric.server_setup
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141026
"""

import os

from fabric.api import *
from fabtools import require, user, group, files
from fabtools.vagrant import vagrant

from . import display_msg, run_as_root


def create_swap_file():

    """
    Will create a system swapfile
    """
    display_msg('Creating system swap file')
    if not files.exists('/swapfile'):
        cmds = ['fallocate -l 1G /swapfile', 'chown 600 /swapfile',
                'mkswap /swapfile', 'swapon /swapfile',
                'sh -c \'echo "/swapfile none swap sw 0 0" >> /etc/fstab\'']

        run_as_root(cmds)
        display_msg('Swapfile created', 'success')


def set_timezone():

    """
    Will set the proper timezone
    """
    display_msg('Setting Server Timezone...')
    cmds = ['echo "US/New_York" > /etc/timezone',
            'dpkg-reconfigure -f noninteractive tzdata']

    run_as_root(cmds)
    display_msg('Timezone updated', 'success')


def set_locale():

    """
    Set the correct locale
    """
    display_msg('Setting Server locale...')
    cmds = ['locale-gen en_US en_US.UTF-8',
            'dpkg-reconfigure locales']
    run_as_root(cmds)
    display_msg('Locale updated', 'success')


def setup_deploy_user(env, **kwargs):

    """
    Create new user for deploy only
    """

    display_msg('Checking/Setting up deploy user options')
    if not user.exists(env.deploy_user):
        display_msg('Created new deploy user', 'success')
        user.create(env.deploy_user, system=True)

    if not group.exists(env.deploy_group):
        display_msg('Created new deploy group', 'success')
        group.create(env.deploy_group)
        user.modify(env.deploy_user, group=env.deploy_group)
        require.users.sudoer(env.deploy_user)


def production_system_setup(env, **kwargs):

    """
    Will install baseline packages for getting
    a simple application server up and running
    """

    # Installs system build tools for the system
    display_msg('Installing system build tools...')
    require.deb.install('build-essential', update=True)

    display_msg('Installing system packages...')
    require.deb.packages([
        'libpq-dev',
        'python-dev',
        'python-software-properties',
        'python2.7-dev',
        'libtiff4-dev',
        'libjpeg8-dev',
        'zlib1g-dev',
        'libfreetype6-dev',
        'liblcms2-dev',
        'libwebp-dev',
        'tcl8.5-dev',
        'tk8.5-dev',
        'subversion',
        'git-core',
        'mercurial',
        'ntp'
    ])

    set_locale()
    set_timezone()
    create_swap_file()
    setup_deploy_user(env)

    # display_msg('System basic setup completed...System will not reboot', 'success')
