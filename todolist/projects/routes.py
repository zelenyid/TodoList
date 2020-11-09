from flask import Blueprint
from flask import request, redirect, url_for
from flask_login import current_user, login_required

from todolist.models import Project
from todolist import db

projects = Blueprint('projects', __name__)


@login_required
@projects.route('/add_project', methods=['POST'])
def add_project():
    """
    Add new project to database
    :return: start page with new project
    """
    name = request.form.get('project')
    new_project = Project(name=name, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('main.index'))


@login_required
@projects.route('/update_project/<int:project_id>', methods=['POST'])
def update_project(project_id):
    """
    Update name of project and commit updates to db
    :param project_id: id updated project
    :return: start page with updates
    """
    project = Project.query.filter_by(id=project_id).first()
    name = request.form.get('project_name')
    project.name = name
    db.session.commit()
    return redirect(url_for('main.index'))


@login_required
@projects.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    """
    Delete project by id and commit changes
    :param project_id: id deleted project
    :return: start page without deleted project
    """
    project = Project.query.filter_by(id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.index'))
