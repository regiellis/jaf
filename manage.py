#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf.manage
AUTHOR: Regi E. <regi@persona.io>
CREATE/UPDATE: 20141004
"""

import os
import subprocess
from termcolor import colored
from jaf import create_app
from flask.ext.script import Manager, Shell, Server

# JAF TOOLS / MANAGERS
from jaf_tools.managers.grunt import manager as grunt_manager
from jaf_tools.managers.deploy import manager as deploy_manager

PROJECT_CWD = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.environ.get('FLASK_CONFIG') or 'development')
manager = Manager(app)
manager.help_args = ('-?', '--help')


def _make_shell_context():
    return dict(app=app)


manager.add_command('runserver', Server(port=8000, host='0.0.0.0'))
manager.add_command('develop', Server(use_debugger=True,
                    use_reloader=True, port=8000, host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=_make_shell_context))
manager.add_command('grunt-task', grunt_manager)
manager.add_command('deploy', deploy_manager)

if __name__ == '__main__':
    manager.run()
