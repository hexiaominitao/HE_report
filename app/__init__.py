from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, DOCUMENTS, IMAGES, configure_uploads, patch_request_class
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
filezips = UploadSet('zipfile', DOCUMENTS)
photos = UploadSet('photos', IMAGES)


def creat_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    bootstrap.init_app(app)
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

    configure_uploads(app, filezips)
    configure_uploads(app, photos)
    patch_request_class(app)

    from .main import main as main_bluprint
    app.register_blueprint(main_bluprint)

    return app