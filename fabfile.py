#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf.fabfile
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141026
"""

import os
from fabric.api import *
from fabtools.vagrant import vagrant


# Module imports
from jaf_tools.fabric.server_setup import production_system_setup
from jaf_tools.fabric.python_env import python_env_setup
from jaf_tools.fabric.server_management import setup_production_server
from jaf_tools.fabric.project_management import upload_project_files

#  === Fabfile Settings for Areate ===

"""
Project default configurations for local and production
devopts
"""

env.user = 'vagrant'  # prompt("Username:")
env.dpeloy_user = 'deploy'
env.deploy_group = 'www-data'
env.hosts = ['0.0.0.0']  # prompt("Hostname:") Enter your host name
env.colorize_errors = True
env.project = 'jaf'  # prompt("Project Name:", validate=str)
env.app_directory = '/var/www/app'
env.url = 'jaf.com.local'  # prompt("Server Configuration Url", validate=str)
env.nginx_config = '{}.conf'.format(env.url)
env.project_dir = '{0}/{1}'.format(env.app_directory, env.project)
env.local_venv = os.path.dirname(__file__)
env.template_dir = os.path.abspath('jaf_tools/templates/')


@task
def setup():
    production_system_setup(env)
    python_env_setup(env)
    setup_production_server(env)
    #utils.run_as_root('reboot now')


# @task
# def restart_services():
#     require.python.virtualenv('{0}/{1}/'.format(env.app_directory, env.project))
#     start_gunicorn_server()
#     require.nginx.enabled('{}'.format(env.nginx_config))


@task
def deploy():
    upload_project_files(env)
    # restart_services()
