from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_mail import Mail  # type: ignore
from flask_wtf import CSRFProtect
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()



