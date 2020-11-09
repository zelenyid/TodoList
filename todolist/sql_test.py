import sqlite3

conn = sqlite3.connect('todolistdb.sqlite')
cursor = conn.cursor()

query_1 = cursor.execute('''
    SELECT DISTINCT status FROM task ORDER BY status ASC;
''')

query_2 = cursor.execute(('''
    SELECT project_id, COUNT(id) count_of_tasks FROM task 
    GROUP BY project_id 
    ORDER BY count_of_tasks DESC;
'''))

query_3 = cursor.execute('''
    SELECT project.name, COUNT(task.id)
    FROM project JOIN task ON project.id = task.project_id
    GROUP BY task.project_id
    ORDER BY project.name ASC;
''')

query_4 = cursor.execute('''
    SELECT * FROM task WHERE name LIKE 'N%';
''')

query_5 = cursor.execute('''
    SELECT p.name, COUNT(t.id) 
    FROM project p JOIN task t ON p.id = t.project_id
    WHERE t.name LIKE '%a%'
    GROUP BY t.project_id;
''')

query_6 = cursor.execute('''
    SELECT name, COUNT(*) count FROM task
    GROUP BY name
    HAVING count > 1
    ORDER BY name
''')

query_7 = cursor.execute('''
    SELECT t.name, t.status, COUNT(*) count
    FROM task t JOIN project p ON t.project_id = p.id
    WHERE p.name = 'Garage' GROUP BY t.name, t.status
    HAVING count > 1 ORDER BY count ASC ;
''')

query_8 = cursor.execute('''
    SELECT p.name, COUNT(t.project_id) as count
    FROM task t JOIN project p ON t.project_id = p.id
    WHERE t.status = True GROUP BY t.project_id
    HAVING count > 10 ORDER BY p.id; 
''')

print(list(query_8))
