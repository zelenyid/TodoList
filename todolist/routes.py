from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from todolist.models import Project, Task, User
from todolist.forms import RegistrationForm, LoginForm
from todolist import app, db, bcrypt


@app.route('/home')
@app.route('/')
def index():
    """
    Render start page
    :return: start page
    """
    if current_user.is_authenticated:
        projects = Project.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', projects=projects, tasks=Task)
    else:
        return redirect(url_for('login'))


@login_required
@app.route('/add_project', methods=['POST'])
def add_project():
    """
    Add new project to database
    :return: start page with new project
    """
    name = request.form.get('project')
    new_project = Project(name=name, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('index'))


@login_required
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


@login_required
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


@login_required
def update_priority_done(project_id):
    """
    Update priority done tasks (add +1 when we add new task) for not repeating one priority.
    It allow to show first of all not done tasks and then done tasks
    """
    done_tasks = Task.query.filter_by(status=True, project_id=project_id)
    for task in done_tasks:
        task.priority += 1
        db.session.commit()


@login_required
def update_priority_after_delete(project_id, deleted_task):
    project_tasks = Task.query.filter_by(project_id=project_id)

    for task in project_tasks:
        if task.priority > deleted_task.priority:
            task.priority -= 1
            db.session.commit()


@login_required
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


@login_required
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

@login_required
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


@login_required
@app.route('/priority_down/<int:task_id>', methods=['POST'])
def priority_down(task_id):
    """
    Set for task priority (now_priority + 1)

    :param task_id: id updated task
    :return:
    """
    task_now = Task.query.filter_by(id=task_id).first()
    next_task = Task.query.filter_by(priority=(task_now.priority+1), project_id=task_now.project_id).first()

    if next_task and not next_task.status and not task_now.status:
        task_now.priority += 1
        db.session.commit()
        next_task.priority -= 1
        db.session.commit()

    return redirect(url_for('index'))


@login_required
@app.route('/priority_up/<int:task_id>', methods=['POST'])
def priority_up(task_id):
    """
    Set for task priority (now_priority - 1)

    :param task_id: id updated task
    :return:
    """
    task_now = Task.query.filter_by(id=task_id).first()
    prev_task = Task.query.filter_by(priority=(task_now.priority-1), project_id=task_now.project_id).first()

    if prev_task and not prev_task.status and not task_now.status:
        task_now.priority -= 1
        db.session.commit()
        prev_task.priority += 1
        db.session.commit()

    return redirect(url_for('index'))


@login_required
@app.route('/change_status/<int:task_id>', methods=['POST'])
def change_status(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.status = not task.status
    db.session.commit()

    priority = task.priority
    if task.status:
        tasks = Task.query.filter_by(project_id=task.project_id).all()

        for update_task in tasks:
            if update_task.priority > priority:
                update_task.priority -= 1
                db.session.commit()

            task.priority = Task.query.filter_by(project_id=task.project_id).count()
            db.session.commit()
    else:
        tasks = Task.query.filter_by(project_id=task.project_id, status=True).all()

        for update_task in tasks:
            if update_task.priority < priority:
                update_task.priority += 1
                db.session.commit()

            task.priority = Task.query.filter_by(project_id=task.project_id).count() - len(tasks)
            db.session.commit()

    return redirect(url_for('index'))


@login_required
@app.route('/add_deadline/<int:task_id>', methods=['POST'])
def add_deadline(task_id):
    deadline = request.form.get('task_deadline')

    deadline_date_format = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')

    if deadline_date_format > datetime.now():
        task = Task.query.filter_by(id=task_id).first()
        task.deadline = deadline_date_format

        db.session.commit()

    return redirect(url_for('index'))


@login_required
@app.route('/delete_deadline/<int:task_id>', methods=['POST'])
def delete_deadline(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.deadline = None

    db.session.commit()

    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
