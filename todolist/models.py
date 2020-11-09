from flask_login import UserMixin

from todolist import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('Project', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Project(id={self.id}, name={self.name})'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    priority = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f'Task(id={self.id}, ' \
               f'name={self.name}, status={self.status}, priority={self.priority}, deadline={self.deadline})'
