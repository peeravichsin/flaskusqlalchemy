from . import db
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship




class Login(db.Model):
    __tablename__ = "login"
    id  = db.Column(db.String(21), unique=True, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # one to one with Student
    students = db.relationship("Student")

class Faculty(db.Model):
    __tablename__ = "faculty"
    id  = db.Column(db.String(2), unique=True, primary_key=True, nullable=False)
    faculty_name = db.Column(db.String(255), unique=True, nullable=False)

    # one to many with Major
    majors = db.relationship("Major")

    # one to many with Student
    students = db.relationship("Student")

    
class Major(db.Model):
    __tablename__ = "major"
    id = db.Column(db.String(14), unique=True, primary_key=True, nullable=False)
    major_name = db.Column(db.String(255), unique=True, nullable=False)

    # one to many with Student
    students = db.relationship("Student")
    
    # one to many with StudyPlan
    studyplans = db.relationship("StudyPlan")

    # ForeignKey
    faculty_id = db.Column(db.String(2), ForeignKey('faculty.id'), nullable=False)


class Subject(db.Model):
    __tablename__ = "subject"
    id =db.Column(db.String(6), unique=True, primary_key=True, nullable=False)
    subject_name_th =db.Column(db.String(255), nullable=False)
    subject_name_en =db.Column(db.String(255), nullable=False)
    subject_credit =db.Column(db.Integer, nullable=False)
    subject_prerequisite =db.Column(db.String(255))

class StudyPlan(db.Model):
    __tablename__ = "study_plan"
    id = db.Column(db.String(5), unique=True, primary_key=True, nullable=False)
    plan = db.Column(db.String(255), nullable=False)
    study_plan_years = db.Column(db.String(1), nullable=False)
    semester = db.Column(db.String(1), nullable=False)

    # one to many with Stud
    enrollresults = db.relationship("EnrollResult")

    # ForeignKey
    major_id =db.Column(db.String(255), ForeignKey('major.id'), nullable=False)





class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    student_fname_th = db.Column(db.String(255), nullable=False)
    student_lname_th = db.Column(db.String(255), nullable=False)
    student_fname_en = db.Column(db.String(255), nullable=False)
    student_lname_en = db.Column(db.String(255), nullable=False)
    student_email = db.Column(db.String(120), unique=True, nullable=False)
    study_year = db.Column(db.String(1), nullable=False)

    # one to many with TranScript
    transcripts = db.relationship('TranScript') 

    # ForeignKey 
    login_id  = db.Column(db.String(21), ForeignKey('login.id'),unique=True, nullable=False)
    faculty_id = db.Column(db.String(2), ForeignKey('faculty.id'), nullable=False)
    major_id = db.Column(db.String(14), ForeignKey('major.id'),nullable=False)


class EnrollResult(db.Model):
    __tablename__ = "enroll_result"
    id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    enroll_date = db.Column(db.DateTime, nullable=False)
    credit_total = db.Column(db.Integer, nullable=False)
    enroll_status = db,Column(db.String(1), nullable=False)

    # ForeignKey
    student_id = db.Column(db.String(10), ForeignKey('student.id'), nullable=False)
    study_plan_id = db.Column(db.String(4), ForeignKey('study_plan.id'), nullable=False)

class TranScript(db.Model):
    __tablename__ = "transcript"
    id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    grade = db.Column(db.String(2))
    transcript_status = db.Column(db.String(10), nullable=False)

    # ForeignKey
    student_id = db.Column(db.String(10), ForeignKey('student.id'), nullable=False)
    enroll_result_id = db.Column(db.String(10), ForeignKey('enroll_result.id'), nullable=False)


