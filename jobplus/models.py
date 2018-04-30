# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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

    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(32))
    name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column('password', db.String(64), nullable=False)
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
    website = db.Column(db.String(128))
    # 一句话简介
    oneword_profile = db.Column(db.String(64))
    address = db.Column(db.String(128))
    finance_stage = db.Column(db.String(128), default="A轮")
    field = db.Column(db.String(128))
    # 职位个数
    position_number = db.Column(db.Integer)
    oneword_profile = db.Column(db.String(64))
    # 公司详情
    detail = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('companies', uselist=False))

    def __repr__(self):
        return 'Company {}'.format(self.name)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # salary_min = db.Column(db.Integer, nullable=False)
    # salary_max = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    experience_requirement = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(64), nullable=False, default="北京天安门")
    is_fulltime = db.Column(db.Boolean, default=True)
    degree_requirement = db.Column(db.String(64))

    # 公司信息
    #company_msg = db.Column(db.String(128))
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
    # 职位要求
    job_requirement = db.Column(db.String(128))
    # 职位描述
    job_description = db.Column(db.String(128))
    # 职位个数
    job_number = db.Column(db.Integer)
    # 职位是否上线
    is_online = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Job {}>'.format(self.name)

    @property
    def tag_list(self):
        return self.tags.split('/')

class Delivery(Base):
    __tablename__ = 'delivery'
    #等待企业审核
    STATUS_WAITING = 1 
    #被拒绝
    STATUS_REJECT = 2 
    #简历被接收，等待面试通知
    STATUS_ACCEPT = 3 

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
    # 企业回应 
    response = db.Column(db.String(256))

    @property
    def user(self):
        return User.query.get(self.user_id)
    @property
    def job(self):
        return Job.query.get(self.job_id)

class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    job_experiences = db.Column(db.String(512))
    edu_experiences = db.Column(db.String(512))
    project_experiences = db.Column(db.String(512))

