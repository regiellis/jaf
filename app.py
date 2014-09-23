#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JAF Framework
AUTHOR: Regi E. <regi@persona.io>
CREATE: 20140921

Single focus flask application template built for small
or single page sites
"""

import os

# CORE
from flask import Flask, render_template, abort, g

# EXTENSIONS
from flask.ext.assets import Bundle, Environment
from flask.ext.mail import Mail
from flask.ext.classy import FlaskView
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# INIT EXTENSIONS
mail = Mail()
assets = Environment()
csrf_protect = CsrfProtect()
toolbar = DebugToolbarExtension()


def create_app(config_name):

    """
    Create/Configure/Initialize the app and all of
    its plugins
    """

    app = Flask(__name__)

    app.config.update(
        DEBUG = True,
        SECRET_KEY = os.environ.get('SECRET_KEY') or None,
        SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME') or None,
        TESTING = False,

        MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost',
        MAIL_PORT = os.environ.get('MAIL_PORT') or 1025,
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or False,
        MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False,
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None,
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None,
        DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER') or None,

        # DEBUG TOOLBAR
        DEBUG_TB_ENABLED = False,
        DEBUG_TO_INTERCEPT_REDITECTS = False,
        DEBUG_TB_PROFILER_ENABLED = True,
        DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True,
    )

    register_extensions(app)

    # REQUEST MODS
    @app.before_request
    def work_before_request():
        pass

    @app.teardown_request
    def work_after_teardown(exception=None):
        pass

    # ERROR ROUTES
    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('utils/page-not-found.html'), 404

    @app.errorhandler(403)
    def forbidden(err):
        return render_template('utils/forbidden.html'), 403

    @app.errorhandler(410)
    def resource_gone(err):
        return render_template('utils/page-not-found.html'), 410

    @app.errorhandler(500)
    def server_error(err):
        return render_template('utils/server-error.html'), 500

    @app.errorhandler(503)
    def maintenance_mode(err):
        return render_template('utils/maintenance.html'), 503

    return app


def register_extensions(app):

    """
    Call in all application extensions and register
    them all with the application instance
    """

    assets.init_app(app)
    mail.init_app(app)
    csrf_protect.init_app(app)
    toolbar.init_app(app)

    return None


def register_assets():
    pass


if __name__ == '__main__':
    app.run(reloader=True)
