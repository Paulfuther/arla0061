
class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    MYSQL_PASSWORD = 'root'
    MYSQL_USER = 'root'
    MYSQL_HOST = 'localhost'
    MYSQL_DB = 'work'
    MYSQL_PORT = 3306