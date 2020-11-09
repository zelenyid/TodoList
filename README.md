# TodoList
Test task for RubyGarage

Project use on client: HTML, CSS, JavaScript. On backend: Python (Flask Framework). Database - SQLite.
# Install and run project
```
    git clone https://github.com/zelenyid/TodoList.git
    cd TodoList
    pipenv install
    python3 run.py
```
<p>For running you need to ser environment variables: SECRET_KEY and SQLALCHEMY_DATABASE_URI</p>
SECRET_KEY you can give next steps in python interpreter: 

``` 
    import secrets

    sectets.token_hex(16)
```
SQLALCHEMY_DATABASE_URI it's uri to your database

#### Functional requirements
+ I want to be able to create/update/delete projects (done)
+ I want to be able to add tasks to my project (done)
+ I want to be able to update/delete tasks (done)
+ I want to be able to prioritize tasks into a project (done) 
+ I want to be able to choose deadline for my task (done)
+ I want to be able to mark a task as 'done' (done)
#### Additional functionality
+ It should work like one page WEB application and should use AJAX technology, load and submit data without reloading a page. (not done)
+ It should have user authentication solution and a user should only have access to their own projects and tasks. (done)
+ It should have automated tests for the all functionality (not done)

# SQL
Given tables: 
 - tasks (id, name, status, project_id) 
 - projects (id, name) 

1. Get all statuses, not repeating, alphabetically ordered

```
    SELECT DISTINCT status FROM tasks ORDER BY status ASC;
```
2. Get the count of all tasks in each project, order by tasks count 
descending

```
    SELECT project_id, COUNT(id) count_of_tasks FROM tasks 
    GROUP BY project_id 
    ORDER BY count_of_tasks DESC;
```
3. Get the count of all tasks in each project, order by projects 
names


```
    SELECT projects.name, COUNT(tasks.id)
    FROM projects JOIN tasks ON projects.id = tasks.project_id
    GROUP BY tasks.project_id
    ORDER BY projects.name ASC;
```

4. Get the tasks for all projects having the name beginning with 
"N" letter

```
    SELECT * FROM tasks WHERE name LIKE 'N%';
```

5. Get the list of all projects containing the 'a' letter in the middle of 
the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with 
project_id = NULL

```
    SELECT p.name, COUNT(t.id) 
    FROM projects p JOIN tasks t ON p.id = t.project_id
    WHERE t.name LIKE '%a%'
    GROUP BY t.project_id;
```

6. Get the list of tasks with duplicate names. Order alphabetically 

```
    SELECT name, COUNT(*) count FROM tasks
    GROUP BY name
    HAVING count > 1
    ORDER BY name;
```

7. Get list of tasks having several exact matches of both name and 
status, from the project 'Garage'. Order by matches count

```
    SELECT t.name, t.status, COUNT(*) count
    FROM tasks t JOIN projects p ON t.project_id = p.id
    WHERE p.name = 'Garage' GROUP BY t.name, t.status
    HAVING count > 1 ORDER BY count ASC;
```

8. Get the list of project names having more than 10 tasks in status 
'completed'. Order by project_id 

```
    SELECT p.name, COUNT(t.project_id) as count
    FROM task t JOIN project p ON t.project_id = p.id
    WHERE t.status = 'completed' GROUP BY t.project_id
    HAVING count > 10 ORDER BY p.id; 
```
