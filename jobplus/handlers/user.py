from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from jobplus.forms import PersonalMsgForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    form = PersonalMsgForm(obj=current_user)
    if form.validate_on_submit():
        form.updated_user(current_user)
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)
