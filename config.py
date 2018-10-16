import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess key'
    SQLALCHEMY_COMMIT_ON_TRARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'xxxxxx'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATEBASE = 'db_herep'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                           DRIVER, USERNAME, PASSWORD,
                                                                           HOST, PORT, DATEBASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'xxxxxxx'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATEBASE = 'db_herep'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                           DRIVER, USERNAME, PASSWORD,
                                                                           HOST, PORT, DATEBASE)
    UPLOADED_ZIPFILE_DEST = 'zip'
    PDF_FILE = 'pdf'


class TestingConfig(Config):
    TESTING = True
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'xxxxxx'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATEBASE = 'db_herep'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                           DRIVER, USERNAME, PASSWORD,
                                                                           HOST, PORT, DATEBASE)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
