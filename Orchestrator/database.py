from flask_sqlalchemy import SQLAlchemy

db = None

def setup_db(app, db_name='test.db'):
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../{db_name}'
    db = SQLAlchemy(app)
    print(f'Setting up uri')