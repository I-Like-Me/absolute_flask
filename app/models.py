from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    versions = db.relationship('Version', backref='program', lazy='dynamic')

    def __repr__(self):
        return f'<App {self.name}>'


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fake_key = db.Column(db.String(64), index=True, unique=True)
    true_key = db.Column(db.String(64), index=True, unique=True)
    app_id = db.Column(db.Integer, db.ForeignKey('app.id'))

    def __repr__(self):
        return f'<Version {self.fake_key}>'
    




