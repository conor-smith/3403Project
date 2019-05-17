from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.globals.update(getat=getattr)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Login manager
login = LoginManager()
login.init_app(app)
# Admin interface
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
admin = Admin(app, template_mode='bootstrap3', base_template='admin/base.html')

from app import routes, models, errors