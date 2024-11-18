# DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'

# SECRET_KEY = 'shhhh... its secret'
# SECURITY_TRACKABLE = True
# SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

class Config():
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'

    SECRET_KEY = 'shhhh... its secret'
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'donot-reply@a.com'

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 2
    CACHE_KEY_PREFIX = 'api_cache'
    CACHE_DEFAULT_TIMEOUT = 60

class ProductionConfig(Config):
    # DEBUG = False
    pass


class celeryConfig():
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    timezone = 'Asia/Kolkata'


