#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools.fabric.python_env
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141026
"""

import os
import yaml

from fabric.api import *
from fabric.contrib.files import append
from fabtools import require, utils, files, python

from . import display_msg
from database_setup import setup_database


def install_application_packages(env, **kwargs):

    """
    Creates a standalone environment for the application to run in.
    Will copy over and install all python packages needed for the
    project.
    """
    project_dir = '{0}/{1}'.format(env.app_directory, env.project)

    display_msg('Creating virtualenv for project...')
    if not files.is_dir(project_dir):
        utils.run_as_root('cd {0} && mkdir {1}'.format(env.app_directory, env.project))

    utils.run_as_root('cd {0} && virtualenv {1}'.format(env.app_directory, env.project))

    with python.virtualenv(project_dir):
        put(os.path.join(env.template_dir, 'requirements.txt'), '/tmp/')
        python.install_requirements('/tmp/requirements.txt')

    display_msg('Project python packages installed', 'success')
    setup_database(env)
    create_production_exports(env, project_dir=project_dir)


def create_production_exports(env, **kwargs):

    display_msg('Exporting environment vars for project...')
    with open(os.path.join(env.template_dir, 'exports')) as export_file:
        export_file = yaml.safe_load(export_file)

        with cd('{}/bin/'.format(kwargs['project_dir'])):
            for key, export in export_file['EXPORTS'].iteritems():
                append('activate', 'export {0}={1}'.format(key, export))

    display_msg('Exporting completed', 'success')


def python_env_setup(env, **kwargs):

    """
    Installs python development tools and env
    """
    display_msg('Installing python environment...')
    if not require.python.is_pip_installed():
        require.python.install_pip()

    require.python.install(['virtualenv', 'virtualenvwrapper', 'ipython',
                            'bpython'], use_sudo=True)

    display_msg('Python environment installed', 'success')
    install_application_packages(env)
