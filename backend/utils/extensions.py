from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_mail import Mail  # type: ignore
db = SQLAlchemy()
mail = Mail()