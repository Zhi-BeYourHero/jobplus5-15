from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime 

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

#必须设置，否则会报sqlalchemy.exc.NoForeignKeysError
#sqlalchemy.exc.NoForeignKeysError: Could not determine join condition between parent/child tables on relationship Job.company - there are no foreign keys linking these tables. Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or specify a 'primaryjoin' expression
user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'))

)

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key = True)
    real_name = db.Column(db.String(32))
    name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    phone = db.Column(db.String(11))
    work_years = db.Column(db.SmallInteger)
    resume_url = db.Column(db.String(128))
    company_msg = db.relationship('Company', uselist=False)
    is_disable = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, set_password):
        self._password = generate_password_hash(set_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)
    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __repr__(self):
        return 'User {}'.format(self.name)

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(64))
    website = db.Column(db.String(512))
    #一句话简介
    oneword_profile = db.Column(db.String(64))
    #finance_stage = db.Column(db.String(128))
    address = db.Column(db.String(128))
    #职位个数
    position_number = db.Column(db.Integer)
    oneword_profile = db.Column(db.String(64))
    #公司详情
    detail = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('companies', uselist=False))


    def __repr__(self):
        return 'Company {}'.format(self.name)

class Job(Base):
    __tablename__  = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    salary_min = db.Column(db.Integer, nullable=False)
    salary_max = db.Column(db.Integer, nullable=False)
    experience_requirement = db.Column(db.String(1024) , nullable=False)
    tags = db.Column(db.String(128))
    degree_requirement = db.Column(db.String(64))
    is_fulltime = db.Column(db.Boolean, default=True)
    address = db.Column(db.String(64), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
    #职位要求
    job_requirement = db.Column(db.String(128))
    #职位描述
    job_description = db.Column(db.String(128))
    #职位个数
    job_number = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Job {}>'.format(self.name)

    @property
    def tag_list(self):
        return self.tags.split(',')
    
