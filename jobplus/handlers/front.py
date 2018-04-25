# coding:utf-8
from flask import render_template,redirect,url_for,Blueprint
from flask_login import login_user,logout_user,login_required
from flask_wtf import Form
from jobplus.forms import LoginForm,RegisterForm
from jobplus.forms import User,db

front = Blueprint('front',__name__)

# Home页设计还没完成
@front.route('/')
def index():
    return render_template('index.html')


@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user.is_disable:
            flash('user had been banned')
            return redierct(url_for('front.login'))
        #判断用户角色,在models有定义
        else:
            login_user(user,form.remember_me.data)
            next = 'user.profile'
            if user.is_admin:
                next = 'admin.index'
            elif user.is_company:
                next = 'company.profile'
            return redirect(url_for('next'))
    return render_template('login.html',form=form)

@front.route('/logout')
@login_required    #若没有登录则不能浏览
def logout():
    logout_user()
    return redirect(url_for('front.index'))   #登出回到Home页


@front.route('/personalregister',methods=['GET','POST'])
def personalregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()   #create_user()函数包含session.add()
        return redirect(url_for('front.login'))
    return render_template('personalregister.html',form=form)
            
@front.route('/companyregister',methods=['GET','POST'])
def companyregister():
    form = RegisterForm()
    if form.validate_on_submit():
        company = form.create_user()
        company.role = User.ROLE_COMPANY    #设置成公司用户
        db.session.add(company)    #提交到Company表
        db.session.commit()
        return redirect(url_for('front.login'))
    return render_template('companyregister.html',form=form)

