#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools.fabric.project_management
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141110
"""

import os
import subprocess32

from fabric import *
from fabric.operations import local, run
from fabric.contrib.project import rsync_project
from fabric.context_managers import prefix, lcd, cd
from fabric.contrib.files import exists

# Module imports
from . import run_as_root
from jaf_tools.fabric.python_env import python_env_setup
from jaf_tools.fabric.server_management import reload_production_server, \
    reload_application_server


def upload_project_files(env, **kwargs):

    """Sync files from local to remote production servers
    """

    if not exists(env.project_dir):
        python_env_setup()

    # Run a clean build on out assests
    asset_build(env)
    # with virtualenv('{0}/{1}'.format(env.app_directory, env.project)):
    #     with cd('{0}/{1}/{1}'.format(env.app_directory, env.project)):

    excluded = ['.*', '*.pyc', '*.log', 'jaf_tools/frontend/', 'jaf_tools/templates/',
                'jaf_tools/fabric/', 'requirements.txt', 'Vagrantfile',
                'fabfile.py', 'tests/']
    rsync_project(remote_dir='{0}/{1}/'.format(env.app_directory, env.project),
                  exclude=excluded)

    update_project_permissions(env)

    # start_gunicorn_server()
    # require.nginx.enabled('{}'.format(env.nginx_config))


def asset_build(env):
    with lcd(env.local_venv):
        with prefix('workon {}'.format(env.project)):
            subprocess32.call(['python manage.py grunt_task build'], shell=True)


def update_project_permissions(env):
    cmds = ['chmod -R 777 static/images/*'.format(env.project_dir, env.project),
            'chown -R 777 {0}/{0} .'.format(env.user)]
    with cd('{0}/{1}/{1}/{1}'.format(env.app_directory, env.project)):  # TODO: CLEAN UP
        run_as_root(cmds)
