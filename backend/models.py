from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weeks = db.relationship("Week", backref="course", lazy=True)

    def __repr__(self):
        return f"Course('{self.name}')"


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    lectures = db.relationship("Lecture", backref="week", lazy=True)
    coding_questions = db.relationship("CodingQuestion", backref="week", lazy=True)

    def __repr__(self):
        return f"Week('{self.number}', '{self.course.name}')"


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    lecture_url = db.Column(db.String(255), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)

    def __repr__(self):
        return f"Lecture('{self.title}', '{self.lecture_url}', '{self.week.number}')"


class CodingQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.Text, nullable=False)
    test_cases = db.Column(db.Text, nullable=False)  # Assuming JSON format for test cases
    code_snippet = db.Column(db.Text, nullable=True)
    solution = db.Column(db.Text, nullable=True)  # Field for the solution
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)
    submissions = db.relationship("Submission", backref="coding_question", lazy=True)

    def __repr__(self):
        return f"CodingQuestion('{self.content}', '{self.week.number}')"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    coding_question_id = db.Column(
        db.Integer, db.ForeignKey("coding_question.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')

    def __repr__(self):
        return f"Submission('{self.code}', '{self.status}')"