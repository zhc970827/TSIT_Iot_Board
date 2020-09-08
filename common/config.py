class Config(object):
    # 通用配置
    pass

class DevConfig(Config):
    ENV_NAME = 'DEV'
    # 开发环境配置
    DEBUG = True
    PORT = 8000

    # 关系型数据库配置
    MYSQL_HOST = "39.105.195.48"
    MYSQL_PORT = 3369
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    # 非关系型数据库配置
    REDIS_HOST = "39.105.195.48"
    REDIS_PORT = 6379
    REDIS_PASSWORD = "123456"

class ReleaseConfig(Config):
    ENV_NAME = 'Release'
    # 发布环境配置
    pass

# TODO 更改配置需要修改  LocalConfig ReleaseConfig
app_config = DevConfig