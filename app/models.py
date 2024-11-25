from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text)
    category = db.Column(db.String(6))
    year = db.Column(db.Date)

    def __repr__(self):
        return f'<Paper {self.title}>'
