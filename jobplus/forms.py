from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import User, db, Company 

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class UserRegisterForm(FlaskForm):
    name = StringField('用户名', validators=[Required(), Length(6,24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已存在')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')


    def create_user(self):
        user = User(name=self.name.data,
            email=self.email.data,
            password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user
        

class CompanyRegisterForm(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(6,24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('企业名称已存在')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')


    def create_company(self):
        user = User(name=self.name.data,
            email=self.email.data,
            password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class PersonalMsgForm(FlaskForm):
    name = StringField('姓名')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume_url = StringField('上传简历')
    submit = SubmitField('提交')
    
    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13','15','18') and len(phone) != 11:
            raise ValidationError('请输入有效手机号码')

    def updated_user(self, user):
        user.real_name = self.name.data
        user.email = self.email.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()



class CompanyMsgForm(FlaskForm):
    name = StringField('姓名')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    phone = StringField('手机号')
    slug = StringField('Slug', validators=[Required(), Length(4,24)])
    address = StringField('地址', validators=[Length(4,64)])
    website = StringField('公司网站')
    logo = StringField('Logo')
    oneword_profile = StringField('一句话描述', validators=[Length(0,64)])
    detail = TextAreaField('公司详情', validators=[Length(0,1024)])
    submit = SubmitField('提交')
    
    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13','15','18') and len(phone) != 11:
            raise ValidationError('请输入有效手机号码')

    def updated_profile(self, company):
        company.name = self.name.data
        company.email = self.email.data
        company.phone = self.phone.data
        if self.password.data:
            company.password = self.password.data
        
        company.slug = self.slug.data
        company.address = self.address.data
        company.website = self.website.data
        company.logo = self.logo.data
        company.oneword_profile = self.oneword_profile.data
        company.detail = self.detail.data
        db.session.add(company)
        db.session.commit()
