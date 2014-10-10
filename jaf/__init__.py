#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JAF TEMPLATE - PROJET NAME HERE
AUTHOR: Regi E. <regi@persona.io>
CREATE: 20140921

A Single focus flask application template built for small
or SPA projects. This setup should only be used for extremely
simple and small projects that require one to three pages of
content.

Simple functions for forms, saving information to a database
or calling information from a api can be contain external files.
But all functions should be imported and registered on the project
in this file.

Flask= Aassets - http://flask-assets.readthedocs.org/en/latest/
Flask-Classy - https://pythonhosted.org/Flask-Classy/
Flask-Mail - https://pythonhosted.org/flask-mail/


"""

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pprint import pprint

# CORE
from flask import Flask, render_template, abort, g

# EXTENSIONS
from flask.ext.assets import Bundle, Environment
from flask.ext.mail import Mail
from flask.ext.classy import FlaskView, route
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension

from settings import config


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# INIT EXTENSIONS
mail = Mail()
assets = Environment()
csrf_protect = CsrfProtect()
toolbar = DebugToolbarExtension()


def create_app(config_name):

    """
    create/configure/initialize the project and all of
    its plugins
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    register_assets(app)
    register_error_handlers(app)
    register_request_mods(app)
    register_views(app)

    register_logging(app)

    return app


def register_logging(app):

    """
    Project basic logging configuration
    """

    mail_server = app.config['MAIL_SERVER']
    server_addr = app.config['DEFAULT_MAIL_SENDER']
    send_addr = app.config['ADMIN']
    error_msg = 'Application Failure'

    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y%m%d-%H:%M%p',
    )

    # MAIL ADMINS ON ERROR
    if not app.config['DEBUG']:
        mail_handler = SMTPHandler(mail_server, server_addr, send_addr, error_msg)
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter('''
        Message Type:          %(levelname)s
        Location:              %(pathname)s:%(lineno)d
        Module:                %(module)s
        Function:              %(funcName)s
        Time:                  %(asctime)s

        Message:

        %(message)s
        '''))
        app.logger.addHandler(mail_handler)

    # FILE LOGGER
        file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    return None


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


def register_assets(app):

    """
    Call in all project assets and register on the
    application. This should only be used if we are
    not running grunt. See Config
    """

    if app.config['GRUNT_MANAGED']:
        core_scripts = Bundle('scripts/libs/jquery/jquery.js',
                              'scripts/libs/modernizr/modernizr.js',
                              'scripts/libs/pubsub-js/pubsub.js',
                              output='scripts/core_libs.js')

        core_styles = Bundle('styles/libs/normalize-less/normalize.css',
                             filters='cssmin', output='styles/core_libs.css')

        assets = Environment()

        assets.register('core_scripts', core_scripts)
        assets.register('core_styles', core_styles)
    else:
        pass

    return None


def register_error_handlers(app):

    """
    Call in global error handlers for the project
    """

    # ERROR ROUTES
    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('jaf/template_page_not_found.html'), 404

    @app.errorhandler(403)
    def forbidden(err):
        return render_template('jaf/template_forbidden.html'), 403

    @app.errorhandler(410)
    def resource_gone(err):
        return render_template('jaf/template_page_not_found.html'), 410

    @app.errorhandler(500)
    def server_error(err):
        return render_template('jaf/template_server_error.html'), 500

    @app.errorhandler(503)
    def maintenance_mode(err):
        return render_template('jaf/template_maintenance.html'), 503

    return None


def register_request_mods(app):

    """
    Alter any of the project request mods here
    """

    # REQUEST MODS
    @app.before_request
    def work_before_request():
        pass

    @app.teardown_request
    def work_after_teardown(exception=None):
        pass

    return None


def register_views(app):

    """
    Project Rotutes
    """

    class HomepageView(FlaskView):
        route_base = '/'

        def index(self):
            return render_template('jaf/template_homepage.html')

    HomepageView.register(app)
    return None
