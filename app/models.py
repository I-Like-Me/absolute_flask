from datetime import datetime
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    entries = db.relationship('Log_Entry', backref='tech', lazy='dynamic')
    requests = db.relationship('Request', backref='caller', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_my_requests(self):
        return Request.query.filter_by(user_id=self.id)

class Log_Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Log_Entry {self.body}>'
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceName = db.Column(db.String(140))
    username = db.Column(db.String(140))
    serialNumber = db.Column(db.String(140))
    localIp = db.Column(db.String(140))
    systemModel = db.Column(db.String(140))
    systemManufacturer = db.Column(db.String(140))
    macAddress = db.Column(db.String(140))
    cortex = db.Column(db.String(140))
    insightVM = db.Column(db.String(140))
    lastConnected = db.Column(db.String(140))
    freeSpace = db.Column(db.String(140))
    citrixVersion = db.Column(db.String(140))
    bitLockKey = db.Column(db.String(140))
    osLevel = db.Column(db.String(140))
    keyTypeUsed = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 

    def __repr__(self):
        return f'<Request {self.deviceName}>'
    


