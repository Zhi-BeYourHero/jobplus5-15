from flask import Blueprint, redirect, flash, url_for, render_template, request, current_app, abort
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm, JobForm
from jobplus.models import User, Job, db, Delivery


company = Blueprint('company',__name__, url_prefix='/company')

@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('你不是企业用户','warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company_msg)
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
    return render_template('company/company_msg.html',  company=company, active='', panel='jobs')

@company.route('/<int:company_id>/admin_index')
@login_required
def admin_index(company_id):
    page = request.args.get('page', default=1,type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('company/admin_index.html', company_id=company_id, pagination=pagination)


@company.route('/<int:company_id>/admin/job/new', methods=['GET','POST'])
@login_required
def admin_add_job(company_id):
    if current_user.id != company_id:
        abort(404)
    form = JobForm()
    if form.validate_on_submit():
        job = form.create_job(current_user)
        db.session.add(job)
        db.session.commit()
        flash('职位创建成功', 'success')
        return redirect(url_for('company.admin_index', company_id=current_user.id))
    return render_template('company/admin_add_job.html', form=form, company_id=company_id)

@company.route('/<int:company_id>/admin/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_job(company_id, job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.id != company_id or job.company_id != current_user.id:
        abort(404)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功', 'success')
        return redirect(url_for('company.admin_index', company_id=company_id))
    return render_template('company/admin_edit_job.html', form=form, company_id=company_id, job=job)


@company.route('/<int:company_id>/admin/job/<int:job_id>/delete')
@login_required
def admin_delete_job(company_id, job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.id != company_id or job.company_id != current_user.id:
        abort(404)
    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功', 'success')
    return redirect(url_for('company.admin_index', company_id=current_user.id))


@company.route('/<int:company_id>/admin/apply')
@login_required
def admin_apply(company_id):
    if not current_user.is_admin and not current_user.id == company_id:
        abort(404)
    status = request.args.get('status', 'all')
    page = request.args.get('page', default=1, type=int)
    deli = Delivery.query.filter_by(company_id=company_id)
    if status == 'waiting':
        deli = deli.filter(Delivery.status==Delivery.STATUS_WAITING)
    elif status == "accept":
        deli = deli.filter(Delivery.status==Delivery.STATUS_ACCEPT)
    elif status == "reject":
        deli = deli.filter(Delivery.status==Delivery.STATUS_REJECT)
    pagination = deli.order_by(Delivery.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('company/admin_apply.html', pagination=pagination, company_id=company_id)


@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/reject/')
@login_required
def admin_apply_reject(company_id, delivery_id):
    deli = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    deli.status = Delivery.STATUS_ACCEPT
    flash('成功拒绝该投递', 'success')
    db.session.add(deli)
    db.session.commit()
    return redirect(url_for('company.admin_apply', company_id=company_id))

@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/accept/')
@login_required
def admin_apply_accept(company_id, delivery_id):
    deli = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    deli.status = Delivery.STATUS.ACCEPT
    flash('成功接受该投递', 'success')
    db.session.add(deli)
    db.session.commit()
    return redirect(url_for('company.admin_apply', company_id=company_id))
