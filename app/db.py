from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.base import Base

db = SQLAlchemy()
migrate = Migrate()