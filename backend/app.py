import os
import atexit
import  logging
from flask import Flask, request #type: ignore
from flask_admin import Admin #type: ignore
from flask_admin.contrib.sqla import ModelView #type: ignore
from flask_cors import CORS #type: ignore
from flask_migrate import Migrate #type: ignore
from configuration.config import Config
from utils.extensions import db, mail, csrf
from routes.auth_route import auth_bp
from routes.assistant_route import chat_bp
from routes.fuel_logs_route import fuel_log_bp
from routes.service_reminders_route import service_reminder_bp
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
from apscheduler.schedulers.background import  BackgroundScheduler #type: ignore
from flask_jwt_extended import JWTManager #type:ignore
from routes.contact_form_route import contact_bp
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #type:ignore
from flask_wtf import CSRFProtect #type:ignore
from flask_talisman import Talisman #type:ignore
from flask_limiter import Limiter #type:ignore
from flask_limiter.util import get_remote_address #type:ignore
from datetime import timedelta
from routes.admin_route import admin_bp
from view.safe_model_view import UserAdmin,BaseSecureModelView





# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.register_blueprint(fuel_log_bp, url_prefix="/vehicle")

def create_app():
    CORS(app, 
         supports_credentials=True, 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )    
    app.config.from_object(Config)

    
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    csrf.exempt(auth_bp)
    csrf.exempt(chat_bp)
    csrf.exempt(fuel_log_bp)
    csrf.exempt(service_reminder_bp)
    csrf.exempt(contact_bp)
    csrf.exempt(admin_bp)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "admin_auth.login" 

    @login_manager.user_loader
    def load_user(user_id):
        from models.User import User
        return User.query.get(int(user_id))



 
    Talisman(app, content_security_policy=None) 
    limiter = Limiter( key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
    limiter.exempt(admin_bp)
    limiter.exempt(auth_bp)


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(service_reminder_bp, url_prefix="/service-reminders")
    app.register_blueprint(contact_bp, url_prefix="/form")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    admin = Admin(app, name="AutoLog Admin", template_mode="bootstrap3")
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(BaseSecureModelView(FuelLog, db.session))
    admin.add_view(BaseSecureModelView(ServiceReminders, db.session))

     
    scheduler = BackgroundScheduler()
    app.scheduler = scheduler
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    logger.info("APScheduler started")

    with app.app_context():
        db.create_all()
        print(app.url_map)
        if not scheduler.running:
            scheduler.start()
            logger.info("Database tables created")
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
