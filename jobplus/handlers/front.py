from flask import Blueprint, render_template, flash, url_for, redirect
from jobplus.forms import LoginForm, UserRegisterForm, CompanyRegisterForm
from jobplus.models import User, db, Job
from flask_login import login_user, logout_user, login_required

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

@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash('用户已经被禁用')
            return redirect(url_for('front.login'))
        else:

            login_user(user, form.remember_me.data)
            target_page = 'user.profile'
            if user.is_company:
                target_page = 'company.profile'
            elif user.is_admin:
                target_page = 'admin.index'
            return redirect(url_for(target_page))
    return render_template('login.html', form=form)

@front.route('/userregister', methods=['GET','POST'])
def userregister():
    form = UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('个人用户注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('userregister.html',form=form)

@front.route('/companyregister', methods=['GET','POST'])
def companyregister():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        enterprise_user = form.create_company()
        enterprise_user.role = User.ROLE_COMPANY
        db.session.add(enterprise_user)
        db.session.commit()
        flash('企业用户注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('companyregister.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))
