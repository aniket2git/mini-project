from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="user")

    purchases=db.relationship(
        "Purchase",
        backref="user",
        lazy=True
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Integer, nullable=False)

    image = db.Column(db.String(300), nullable=True)

    lectures=db.relationship(
        "Lecture",
        backref="course",
        lazy=True
    )
    purchases=db.relationship(
        "Purchase",
        backref="course",
        lazy=True
    )

    def __repr__(self):
        return f"Course('{self.title}', '{self.price}')"
    
class Lecture(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    video_url = db.Column(db.String(500), nullable=False)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    def __repr__(self):
        return f"Lecture('{self.title}')"
    
class Purchase(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    def __repr__(self):
        return f"Purchase(User: {self.user_id}, Course: {self.course_id})"