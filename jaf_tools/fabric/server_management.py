#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf_tools.fabric.server_management
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141110
"""

import os
from fabtools import require


def setup_production_server(env, **kwargs):

    """Configures nginx server for production
    """
    require.nginx.server()
    nginx_template = file(os.path.join(env.template_dir, 'nginx')).read()
    docroot = '{0}/{1}'.format(env.app_directory, env.project)
    project = '{0}/{0}'.format(env.project)

    require.nginx.site(
        env.url,
        template_contents=nginx_template,
        port=80,
        server_alias='www.{}'.format(env.url),
        proxy_url="127.0.0.1:8080",
        docroot=docroot,
        project=project
    )


def rebuild_production_server(env, **kwargs):

    """Removes old nginx template file and replace it with a new template
    """
    pass


def reload_production_server(env, **kwargs):

    """Reload nginx server
    """
    pass


def setup_application_server(env, **kwargs):

    """Setups and configs new gunicorn application server
    """
    pass


def reload_application_server(env, **kwargs):

    """Reloads application server configurations
    """
    pass

# def start_gunicorn_server():
#     create_production_exports()
#     with virtualenv('{0}/{1}'.format(env.app_directory, env.project)):
#         with cd('{0}/{1}/{1}'.format(env.app_directory, env.project)):
#             run('gunicorn -b 127.0.0.1:8080 --workers=4 server:app', shell=True)
