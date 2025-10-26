from flask_cors import CORS
import atexit
import logging
from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from configuration.config import Config
from utils.extensions import db, mail, csrf
from routes.auth_route import auth_bp
from routes.assistant_route import chat_bp
from routes.fuel_logs_route import fuel_log_bp
from routes.service_reminders_route import service_reminder_bp
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import JWTManager
from routes.contact_form_route import contact_bp
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes.admin_route import admin_bp
from view.safe_model_view import UserAdmin, BaseSecureModelView
from routes.dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS configuration with proper credentials support
    CORS(app, 
         supports_credentials=True, 
         origins=[
             "http://localhost:4200",
             "http://127.0.0.1:4200",  # Added for Angular dev server
             "https://autolog-backend-7961ac6afab3.herokuapp.com"
         ])

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # CSRF exemptions
    csrf.exempt(auth_bp)
    csrf.exempt(chat_bp)
    csrf.exempt(fuel_log_bp)
    csrf.exempt(service_reminder_bp)
    csrf.exempt(contact_bp)
    csrf.exempt(admin_bp)
    csrf.exempt(dashboard_bp)

    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Flask-Login configuration
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "admin_auth.login"  # Blueprint endpoint
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            logging.error(f"Error loading user: {e}")
            return None

    # Security middleware
    Talisman(app, content_security_policy=None)
    
    # Rate limiting
    limiter = Limiter(
        key_func=get_remote_address, 
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)
    limiter.exempt(admin_bp)
    limiter.exempt(auth_bp)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(fuel_log_bp, url_prefix="/vehicle")
    app.register_blueprint(service_reminder_bp, url_prefix="/service-reminders")
    app.register_blueprint(contact_bp, url_prefix="/form")
    app.register_blueprint(admin_bp, url_prefix="/admin_auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # Flask-Admin configuration
    admin = Admin(app, name="AutoLog Admin", template_mode="bootstrap3", url="/admin")
    admin.add_view(UserAdmin(User, db.session, name="Users", category="Models"))
    admin.add_view(BaseSecureModelView(FuelLog, db.session, name="Fuel Logs", category="Models"))
    admin.add_view(BaseSecureModelView(ServiceReminders, db.session, name="Service Reminders", category="Models"))

    # Scheduler setup
    scheduler = BackgroundScheduler()
    app.scheduler = scheduler
    scheduler.start()
    
    # Proper shutdown handling
    def shutdown_scheduler():
        if scheduler.running:
            scheduler.shutdown()
    
    atexit.register(shutdown_scheduler)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
            logger.info("Application started successfully")
        except Exception as e:
            logger.error(f"Database creation error: {e}")
            raise

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)