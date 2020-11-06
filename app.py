import os

from flask import Flask, render_template, url_for


# Init app
app = Flask(__name__)

projects = [
    {
        'id': 1,
        'name': 'Complete the test task for Ruby Garage',
    },
    {
        'id': 2,
        'name': 'For Home',
    },
]

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
def hello_world():
    return render_template('index.html', projects=projects, tasks=tasks)


# Next two function to sent to static file additional param and render html files with css (Don't touch!)
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# Run server
if __name__ == '__main__':
    app.run()
