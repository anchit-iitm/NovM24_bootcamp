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

class ProductionConfig(Config):
    # DEBUG = False
    pass





