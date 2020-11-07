from flask import render_template, request, redirect, url_for

from todolist.models import Project, Task

from todolist import app, db


@app.route('/')
def index():
    """
    Render start page
    :return: start page
    """
    projects = Project.query.all()
    tasks = Task.query.all()
    return render_template('index.html', projects=projects, tasks=Task)


@app.route('/add_project', methods=['POST'])
def add_project():
    """
    Add new project to database
    :return: start page with new project
    """
    name = request.form.get('project')
    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update_project/<int:project_id>', methods=['POST'])
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
    return redirect(url_for('index'))


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    """
    Delete project by id and commit changes
    :param project_id: id deleted project
    :return: start page without deleted project
    """
    project = Project.query.filter_by(id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


def update_priority_done(project_id):
    """
    Update priority done tasks (add +1 when we add new task) for not repeating one priority.
    It allow to show first of all not done tasks and then done tasks
    """
    done_tasks = Task.query.filter_by(status=True, project_id=project_id)
    for task in done_tasks:
        task.priority += 1
        db.session.commit()


def update_priority_after_delete(project_id, deleted_task):
    project_tasks = Task.query.filter_by(project_id=project_id)

    for task in project_tasks:
        if task.priority > deleted_task.priority:
            task.priority -= 1
            db.session.commit()


@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    """
    Add task to project
    :param project_id: project's id
    :return: start page with new task
    """
    name = request.form.get('task_title')
    status = False
    priority = Task.query.filter_by(project_id=project_id).count() - Task.query.filter_by(status=True,
                                                                                          project_id=project_id).count() + 1

    update_priority_done(project_id)

    new_task = Task(name=name, status=status, priority=priority, project_id=project_id)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Delete task from project
    :param task_id: deleted task
    :return: start page without deleted task
    """
    task = Task.query.filter_by(id=task_id).first()

    update_priority_after_delete(task.project_id, task)

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update_task_title/<int:task_id>', methods=['POST'])
def update_task_title(task_id):
    """
    Update name of task and commit updates to db
    :param task_id: id updated task
    :return: start page with updates
    """
    task = Task.query.filter_by(id=task_id).first()
    name = request.form.get('task_name')
    task.name = name
    db.session.commit()
    return redirect(url_for('index'))
