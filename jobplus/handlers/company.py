from flask import Blueprint, redirect, flash, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from jobplus.forms import CompanyMsgForm
from jobplus.models import User

company = Blueprint('company',__name__, url_prefix='/company')

@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('你不是企业用户','warning')
        return redirect(url_for('front.index'))
    form = CompanyMsgForm(obj=current_user.company_msg)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('更新企业信息成功!', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['COMPANY_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/<int:company_id>')
def company_msg(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is_company:
        abort(404)
    return render_template('company/company_msg.html', company=company, active='', panel='company_description')

@company.route('/<int:company_id>/jobs')
def company_jobs(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is_company:
        abort(404)
    return render_template('company/company_msg.html'. company=company, active='', panel='jobs')

