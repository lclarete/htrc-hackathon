# config.py

class Config:
    SECRET_KEY = '8b3798d5ae564b839f7d279b474f6452'  # Simple secret key
    DATA_FILE = 'data.json'
    PDF_DIRECTORY = 'pdfs'
    PDF_FILENAME = 'charts_output.pdf'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
