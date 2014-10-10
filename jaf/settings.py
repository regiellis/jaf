#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jaf.settings
AUTHOR: Regi E.<regi@persona.io>
CREATE/UPDATED: 20141004
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ProjectConfigs(object):

    """
    Base configuration class for the entire project
    """

    # BASE FLASK CONFIGS
    ADMIN = ['email@somewhere.com', 'errors@somewhere.com']
    DEBUG = True
    MAINTENANCE = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or None
    JSONIFY_PRETTYPRINT_REGULAR = True

    # BASE MAIL CONFIGS
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 1025
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or False
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
    DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER') or 'jaf Application Server'

    GRUNT_MANAGED = True

    # CREATE INSTANCE OF THE APP
    @staticmethod
    def init_app(app):
        pass


class DevelopementConfigs(ProjectConfigs):

    """
    Development Configs for the entire project
    """

    ASSETS_DEBUG = True
    MAINTENANCE = False
    CACHE_TYPE = 'simple'
    SECRET_KEY = 'generate_key_for_development'  # os.urandom()

    # DEBUG TOOLBAR
    DEBUG_TB_ENABLED = False
    DEBUG_TO_INTERCEPT_REDITECTS = False
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True


class ProductionConfigs(ProjectConfigs):

    """
    Prodiction Configs for the entire project
    """

    DEBUG = False
    ASSETS_DEBUG = False
    MAINTENANCE = False


class TestingConfigs(ProjectConfigs):

    """
    Testing Configs for the entire project
    """

    TESTING = True
    MAINTENANCE = False

config = {
    'development': DevelopementConfigs,
    'testing': TestingConfigs,
    'production': ProductionConfigs,
    'defualt': ProjectConfigs
}
