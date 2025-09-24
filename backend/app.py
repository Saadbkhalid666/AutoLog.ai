import os
from flask import Flask # type: ignore
from flask_admin import Admin   # type: ignore
from flask_admin.contrib.sqla import ModelView # type: ignore
from utils.extensions import db
from configuration.config import Config
from routes.auth_route import auth_bp
from models.User import User
from utils.extensions import mail
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from flask_cors import CORS # type: ignore
from routes.assistant_route import chat_bp
 

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/auth/*": {"origins": "http://localhost:4200"}})


    app.config.from_object(Config)
    # Initialize DB
    db.init_app(app)

    mail.init_app(app)
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")

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
