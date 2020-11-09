from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user

from todolist.models import Project, Task


main = Blueprint('main', __name__)


@main.route('/home')
@main.route('/')
def index():
    """
    Render start page
    :return: start page
    """
    if current_user.is_authenticated:
        projects = Project.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', projects=projects, tasks=Task)
    else:
        return redirect(url_for('users.login'))
