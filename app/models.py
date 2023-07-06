from app import db, login
from datetime import datetime
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

class Basic_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    Total_count = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f'<Basic_Viz_Data {self.timestamp}>'

class AD_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<AD_Viz_Data {self.timestamp}>'

class AD_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<AD_LP_Viz_Data {self.timestamp}>'

class AI_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<AI_Viz_Data {self.timestamp}>'

class AI_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<AI_LP_Viz_Data {self.timestamp}>'

class CONF_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<CONF_Viz_Data {self.timestamp}>'

class CS3_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<CS3_Viz_Data {self.timestamp}>'

class CS4_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<CS4_Viz_Data {self.timestamp}>'

class CS_BK_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<CS_BK_Viz_Data {self.timestamp}>'

class CS_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<CS_LP_Viz_Data {self.timestamp}>'

class FAC_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<FAC_Viz_Data {self.timestamp}>'

class FAC_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<FAC_LP_Viz_Data {self.timestamp}>'

class FI_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<FI_LP_Viz_Data {self.timestamp}>'
    
class FI_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<FI_LP_Viz_Data {self.timestamp}>'

class GLOBAL_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<GLOBAL_Viz_Data {self.timestamp}>'

class HPO_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<HPO_Viz_Data {self.timestamp}>'

class HPO_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<HPO_LP_Viz_Data {self.timestamp}>'

class IF_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<IF_Viz_Data {self.timestamp}>'
    
class IF_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<IF_LP_Viz_Data {self.timestamp}>'

class IT_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<IT_Viz_Data {self.timestamp}>'
    
class IT_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<IT_LP_Viz_Data {self.timestamp}>'

class KIT_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<KIT_Viz_Data {self.timestamp}>'
    
class LW_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<LW_Viz_Data {self.timestamp}>'

class LW_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<LW_LP_Viz_Data {self.timestamp}>'

class MC2_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MC2_Viz_Data {self.timestamp}>'

class MC3_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MC3_Viz_Data {self.timestamp}>'

class MC_BK_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MC_BK_Viz_Data {self.timestamp}>'

class MC_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MC_LP_Viz_Data {self.timestamp}>'

class MR_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MR_Viz_Data {self.timestamp}>'

class MR_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<MR_LP_Viz_Data {self.timestamp}>'

class NH_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<NH_Viz_Data {self.timestamp}>'

class NH_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<NH_LP_Viz_Data {self.timestamp}>'

class OFF_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<OFF_Viz_Data {self.timestamp}>'
    
class OPTO_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<OPTO_Viz_Data {self.timestamp}>'

class OPTO_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<OPTO_LP_Viz_Data {self.timestamp}>'

class PA_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PA_Viz_Data {self.timestamp}>'

class PA_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PA_LP_Viz_Data {self.timestamp}>'
    
class PC3_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PC3_Viz_Data {self.timestamp}>'

class PC4_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PC4_Viz_Data {self.timestamp}>'

class PC_BK_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PC_BK_Viz_Data {self.timestamp}>'

class PC_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PC_LP_Viz_Data {self.timestamp}>'
    
class PHA_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PHA_Viz_Data {self.timestamp}>'

class PHA_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PHA_LP_Viz_Data {self.timestamp}>'

class POPUP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<POPUP_Viz_Data {self.timestamp}>'

class PSS_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PSS_LP_Viz_Data {self.timestamp}>'

class PT_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PT_Viz_Data {self.timestamp}>'
    
class PT_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<PT_LP_Viz_Data {self.timestamp}>'

class SP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<SP_Viz_Data {self.timestamp}>' 

class SP_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<SP_LP_Viz_Data {self.timestamp}>'
    
class WH_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<WH_Viz_Data {self.timestamp}>'

class WH_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True) # space
    dept_count = db.Column(db.Integer, index=True) # full
    bit_count = db.Column(db.Integer, index=True) # bitlocker
    ctx_ver_count = db.Column(db.Integer, index=True) # citrix
    zm_ver_count = db.Column(db.Integer, index=True) # zoom
    wpl_ver_count = db.Column(db.Integer, index=True) # windows product level
    cor_count = db.Column(db.Integer, index=True) # cortex
    ivm_count = db.Column(db.Integer, index=True) # ivanti
    dell_count = db.Column(db.Integer, index=True) # make
    lenovo_count = db.Column(db.Integer, index=True) # make
    vul_count = db.Column(db.Integer, index=True) # vulnerability
    exp_count = db.Column(db.Integer, index=True) # exploits
    mal_count = db.Column(db.Integer, index=True) # malware
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<WH_LP_Viz_Data {self.timestamp}>'

class WL_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<WL_Viz_Data {self.timestamp}>'

class WL_LP_Viz_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    space_count = db.Column(db.Integer, index=True)
    dept_count = db.Column(db.Integer, index=True)
    bit_count = db.Column(db.Integer, index=True)
    ctx_ver_count = db.Column(db.Integer, index=True)
    zm_ver_count = db.Column(db.Integer, index=True)
    wpl_ver_count = db.Column(db.Integer, index=True)
    cor_count = db.Column(db.Integer, index=True)
    ivm_count = db.Column(db.Integer, index=True)
    dell_count = db.Column(db.Integer, index=True)
    lenovo_count = db.Column(db.Integer, index=True)
    vul_count = db.Column(db.Integer, index=True)
    exp_count = db.Column(db.Integer, index=True)
    mal_count = db.Column(db.Integer, index=True)
    year_1_count = db.Column(db.Integer, index=True) # age
    year_2_count = db.Column(db.Integer, index=True) # age
    year_3_count = db.Column(db.Integer, index=True) # age
    year_4_count = db.Column(db.Integer, index=True) # age
    year_5_count = db.Column(db.Integer, index=True) # age

    def __repr__(self):
        return f'<WL_LP_Viz_Data {self.timestamp}>'
