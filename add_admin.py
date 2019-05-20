from app import db
from app.models import User
u = User(username='admin', admin = 1)
u.set_password('admin')
db.session.add(u)
db.session.commit()