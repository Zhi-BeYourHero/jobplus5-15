class BaseConfig(object):
    SECRET_KEY = 'SECRET'
    JOB_PER_PAGE = 9 
    COMPANY_PER_PAGE = 12
    ADMIN_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost:3306/jobplus?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }

