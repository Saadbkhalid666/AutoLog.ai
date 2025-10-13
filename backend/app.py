import  logging
from flask import Flask #type: ignore
from flask_admin import Admin #type: ignore
from flask_admin.contrib.sqla import ModelView #type: ignore
from flask_cors import CORS #type: ignore
from flask_migrate import Migrate #type: ignore
from configuration.config import Config
from utils.extensions import db, mail
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


import atexit

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

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(service_reminder_bp, url_prefix="/service-reminders")
    app.register_blueprint(contact_bp, url_prefix="/form")

    admin = Admin(app, name="AutoLog Admin", template_mode="bootstrap3")
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(FuelLog, db.session))
    admin.add_view(ModelView(ServiceReminders, db.session))

    scheduler = BackgroundScheduler()
    app.scheduler = scheduler
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    logger.info("APScheduler started")

    with app.app_context():
        db.create_all()
        if not scheduler.running:
            scheduler.start()
            logger.info("Database tables created")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
