from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Paper(db.Model):
    __bind_key__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text)
    category = db.Column(db.String(6))
    year = db.Column(db.Date)

    def __repr__(self):
        return f'<Paper {self.title}>'


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Citation(db.Model):
    __bind_key__ = 'citation'
    first = db.Column(db.Integer)
    second = db.Column(db.Integer)

    def __repr__(self):
        return f'<Citation {self.first}>'
