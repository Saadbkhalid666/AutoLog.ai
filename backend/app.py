import os
from flask import Flask # type: ignore
from flask_admin import Admin   # type: ignore
from flask_admin.contrib.sqla import ModelView # type: ignore
from config import Config
from utils.db import db
from routes.auth_route import auth_bp
from models.User import User
from flask_mail import Mail # type: ignore
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

mail = Mail()


 

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    # Initialize DB
    db.init_app(app)

    mail.init_app(app)
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Flask-Admin setup
    admin = Admin(app, name="AutoLog Admin", template_mode="bootstrap3")
    admin.add_view(ModelView(User, db.session))

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
