import os


class Config:
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = '9S/OCZkrz6otCShcYsg7CQD2fTIamt4OhLUWOrypb+SXBv25Hs/48r9E7Msxxv0/bI+ifRQrrhxX\nKBFNk77gDw==\n'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(BASE_FOLDER, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_CHECK_DEFAULT = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    pass
