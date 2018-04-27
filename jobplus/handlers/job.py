from flask import Blueprint, request, render_template, current_app, flash, redirect, url_for
from jobplus.models import Job, Delivery, db
from flask_login import login_required, current_user

job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination, active='job')

@job.route('/<int:job_id>')
def job_msg(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/job_msg.html', job=job, active='')


@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if job.current_user_is_applied:
        flash('已经投递过该职位', 'warning')
    else:
        d = Delivery(
            job_id = job.id,
            user_id = current_user.id
        )
        db.session.add(d)
        db.session.commit()
        flash('投递成功', 'sucess')
    return redirect(url_for('job.job_msg', job_id=job.id))

@job.route('/<int:job_id>/downline')
@login_required
def downline(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.id != job.company.id:
        abort(404)
    if not job.is_online:
        flash('职位已经下线', 'warning')
    else:
        job.is_online = False
        db.session.add(job)
        db.session.commit()
        flash('职位下线成功', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))


@job.route('/<int:job_id>/online')
@login_required
def online(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.id != job.company.id:
        abort(404)
    if job.is_online:
        flash('职位已经上线', 'warning')
    else:
        job.is_online = True 
        db.session.add(job)
        db.session.commit()
        flash('职位上线成功', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))
        
