# /config.py

class Config:
    """Base configuration."""
    SECRET_KEY = 'supersecretkey'
    DEBUG = False
    TESTING = False
    HOST = 'localhost'
    PORT = 5000
    # Add any other configuration variables you need here


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
    # Add specific dev configurations, like DB URIs for development
    DATABASE_URI = 'sqlite:///dev.db'


class ProductionConfig(Config):
    """Production configuration."""
    HOST = '0.0.0.0'
    PORT = 8000
    # Add production configurations like external database URIs
    DATABASE_URI = 'mysql://user@localhost/prod_db'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = 'sqlite:///:memory:'
