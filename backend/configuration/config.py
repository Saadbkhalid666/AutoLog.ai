import os
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25)) 
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() in ["true", "1", "t"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # Flask-Login session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=6)  
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask-WTF CSRF configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False  # Disable CSRF by default, enable per route
    
    # Remember me cookie
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_DOMAIN=None