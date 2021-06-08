class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mysecretkey123321'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://onyx:coolPass123@localhost/flask_app'

class TestingConfig(Config):
    TESTING = True
    
    SESSION_COOKIE_SECURE = False
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://onyx:coolPass123@localhost/test_flask_app'