from flask import render_template, request, redirect, url_for

from todolist.models import Project, Task

from todolist import app, db


# projects = [
#     {
#         'id': 1,
#         'name': 'Complete the test task for Ruby Garage',
#     },
#     {
#         'id': 2,
#         'name': 'For Home',
#     },
# ]

tasks = [
    {
        'id': 1,
        'name': 'Open this mock-up in Adobe Fireworks',
        'status': False,
        'deadline': 'April 20, 2020',
        'project_id': 1,
        'priority': 1
    },
    {
        'id': 2,
        'name': 'Attentively check the file',
        'status': False,
        'deadline': 'April 21, 2020',
        'project_id': 1,
        'priority': 2
    },
    {
        'id': 3,
        'name': 'Write HTML & CSS',
        'status': False,
        'deadline': 'April 22, 2020',
        'project_id': 1,
        'priority': 3
    },
    {
        'id': 4,
        'name': 'Add JS',
        'status': False,
        'deadline': 'April 23, 2020',
        'project_id': 1,
        'priority': 4
    },
    {
        'id': 5,
        'name': 'Buy a milk',
        'status': False,
        'deadline': 'April 20, 2020',
        'project_id': 2,
        'priority': 1
    },
    {
        'id': 6,
        'name': 'Call Mam',
        'status': False,
        'deadline': 'April 26, 2020',
        'project_id': 2,
        'priority': 2
    },
    {
        'id': 7,
        'name': 'Clean the room',
        'status': False,
        'deadline': 'April 12, 2020',
        'project_id': 2,
        'priority': 3
    }
]


@app.route('/')
def index():
    """
    Render start page

    :return: start page
    """
    projects = Project.query.all()
    return render_template('index.html', projects=projects, tasks=tasks)


@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form.get('project')
    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('index'))


def edit():
    pass
