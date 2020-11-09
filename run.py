from todolist import create_app, db

app = create_app()

# Run app
if __name__ == '__main__':
    db.create_all()
    app.run()
