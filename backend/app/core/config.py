import os
from datetime import timedelta

# Base configuration class with common settings for all environments
class BaseConfig:
    SECRET_KEY                     = os.getenv("SECRET_KEY", "alkion-dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES       = timedelta(hours=8)
    JWT_REFRESH_TOKEN_EXPIRES      = timedelta(days=30)
    CELERY_BROKER_URL              = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND          = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Development configuration with settings specific to the development environment
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://alkion:alkion@localhost:5432/alkion_dev"
    )
    SQLALCHEMY_ECHO = True

# Production configuration with settings specific to the production environment
class ProductionConfig(BaseConfig):
    DEBUG                   = False
    SQLALCHEMY_ECHO         = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# Testing configuration with settings specific to the testing environment
class TestingConfig(BaseConfig):
    TESTING                 = True
    SQLALCHEMY_ECHO         = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)

# Dictionary to map environment names to their corresponding configuration classes
config_by_name = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}
