from todolist.models import Task
from todolist import db


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
    """
    Change priority (minus 1) that after deleted task
    """
    project_tasks = Task.query.filter_by(project_id=project_id)

    for task in project_tasks:
        if task.priority > deleted_task.priority:
            task.priority -= 1
            db.session.commit()
