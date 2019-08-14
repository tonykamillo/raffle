import os


class Config:
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(BASE_FOLDER, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass
