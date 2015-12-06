#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Andrew Perry'
__email__ = 'ajperry@pansapiens.com'
__version__ = '1'

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask_wtf.csrf import CsrfProtect

from cardboardcam.controllers.main import main
from cardboardcam import assets
from cardboardcam.models import db

from cardboardcam.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)

csrf = CsrfProtect()

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. cardboardcam.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # handler = RotatingFileHandler('cardboardcam.log', maxBytes=10000, backupCount=1)
    handler = StreamHandler()
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    csrf.init_app(app)

    # register our blueprints
    app.register_blueprint(main)

    return app