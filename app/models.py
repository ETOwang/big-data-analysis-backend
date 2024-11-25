from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(255))
    published_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Paper {self.title}>'
