from todolist import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

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
