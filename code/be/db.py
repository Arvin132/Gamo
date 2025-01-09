from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def db_log(message: str):
     print("Data Base Info: " + message)

def initilize_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


def import_user_values():
    users = [
        User(username="MasterMind"),
        User(username="Test1"),
        User(username="Test2")
    ]
    
    # Add all users at once
    db.session.add_all(users)
    # Commit the changes
    db.session.commit() 
    
def init_database(app):
    path_to_db = "instance/my_database.db"
    path_to_db = os.path.abspath(path_to_db)
    if (os.path.exists(path_to_db)):
        os.remove(path_to_db)
        db_log(f"removed the database at location {path_to_db}")
    with app.app_context():
        db.create_all()
        import_user_values()
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Relationship to Bots
    bots = db.relationship('Bot', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Bot(db.Model):
    __tablename__ = 'bots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)

    # Foreign Key relationship with the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Bot {self.name} located at {self.location}>'
    
    
