import  logging
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_migrate import Migrate
from configuration.config import Config
from utils.extensions import db, mail
from routes.auth_route import auth_bp
from routes.assistant_route import chat_bp
from routes.fuel_logs_route import fuel_log_bp
from routes.service_reminders_route import service_reminder_bp
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://192.168.1.7:4200"}}, supports_credentials=True)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(fuel_log_bp, url_prefix="/vehicle")
    app.register_blueprint(service_reminder_bp, url_prefix="/service-reminders")

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
    app.run(host="192.168.1.7", port=5000, debug=True)
