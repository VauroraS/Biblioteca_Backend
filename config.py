from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:admin1234+@localhost/biblioteca_upateco_final')
    SECRET_KEY = os.getenv("SECRET_KEY")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'mysql+pymysql://root:admin1234+@localhost/biblioteca_test')
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  # Evita errores de conexión