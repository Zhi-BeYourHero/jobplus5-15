# coding=utf8
import os
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError,IntegerField
from wtforms.validators import Required,Length,Email,EqualTo
from jobplus.models import db,User
from flask_wtf.file import FileField,FileRequired

class LoginForm(FlaskForm):        #登录页面的内容  
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('email has not register')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('passwrod error')


class RegisterForm(FlaskForm):    #求职者和公司的注册页面内容
    name = StringField('用户名',validators=[Required(),Length(1,64)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repear_password = PasswordField(
        '重复密码',
        validators=[Required(),Length(6,24),
        EqualTo('password',message = '密码要一致')]
    )
    submit = SubmitField('注册')


    def validate_email(self,field):        
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('名已经被注册')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class UserProfileForm(FlaskForm):
    real_name = StringField('name',validators=[Required(),Length(1,64)])
    email = StringField('email',validators=[Required(),Email()])
    password = PasswordField('password(no write no change)')
    phone = StringField('phone number',validators=[Required()])
    work_year = IntegerField('work year')
    resume_url = FileField('upload resume')
    submit = SubmitField('submit')

    def validate_phone(self,field):
        phone = field.data
        if phone[:2] not in ('13','15','18') and len(phone) !=11:
            raise ValidationError('please enter a correct phone number')

    def upload_resume(self):
        f = self.resume.data
        filename = self.real_name.data + '.pdf'
        f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','resume',filename))
        return filename

    def update_profile(self,user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_year = self.work_year.data
        filename = self.upload_resume()
        user.resume_url = url_for('static',filename=os.path.join('resumes',filename))
        db.session.add(user)
        db.session.commit()
