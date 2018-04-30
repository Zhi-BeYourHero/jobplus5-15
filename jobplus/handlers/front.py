# coding:utf-8
from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required
from flask_wtf import Form
from jobplus.forms import LoginForm, RegisterForm
from jobplus.forms import db
from jobplus.models import User, Job

front = Blueprint('front', __name__)


@front.route('/')
def index():
    newest_jobs = Job.query.order_by(Job.created_at.desc()).limit(9)
    newest_companies = User.query.filter(
        User.role == User.ROLE_COMPANY
    ).order_by(User.created_at.desc()).limit(8)
    return render_template(
        'index.html',
        active='index',
        newest_jobs=newest_jobs,
        newest_companies=newest_companies
    )  

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.name_email.data).first():
            user = User.query.filter_by(email=form.name_email.data).first()
        else:
            user = User.query.filter_by(name=form.name_email.data).first()
        if user.is_disable:
            # <<<<<<< HEAD
            flash('用户被禁止')
            return redirect(url_for('front.login'))  # 修正拼写错误
            # 判断用户角色,在models有定义
            '''
         =======
            flash('user had been banned')   # 增加import flash
            return redirect(url_for('front.login'))
        # 判断用户角色,在models有定义
>>>>>>> dev
            '''
        else:
            login_user(user, form.remember_me.data)
            next = 'user.profile'
            if user.is_admin:
                next = 'admin.index'
            elif user.is_company:
                next = 'company.profile'
            return redirect(url_for(next))  # 原文件redierct拼写错误
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required  # 若没有登录则不能浏览
def logout():
    logout_user()
    flash('您已经退出登录', 'success')  # 原文件没有flash
    return redirect(url_for('front.index'))  # 登出回到Home页


@front.route('/personalregister', methods=['GET', 'POST'])
def personalregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()  # create_user()函数包含session.add()
        flash('用户注册成功，请登录', 'success')  # 增加flash展示
        return redirect(url_for('front.login'))
    return render_template('personalregister.html', form=form)


@front.route('/companyregister', methods=['GET', 'POST'])
def companyregister():
    form = RegisterForm()
    form.name.label = u'企业名称'
    if form.validate_on_submit():
        company = form.create_user()
        company.role = User.ROLE_COMPANY  # 设置成公司用户
        db.session.add(company)  # 提交到Company表
        db.session.commit()
        flash('用户注册成功，请登录', 'success')  # 增加flash展示
        return redirect(url_for('front.login'))
    return render_template('companyregister.html', form=form)
