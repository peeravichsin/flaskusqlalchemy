from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import pandas as pd


db = SQLAlchemy()
DB_NAME = "EnrollCheck.db"


def create_app():
    app = Flask(__name__)
    app.secret_key = "ifyouknowyouknowandifyoudontknowyoudontknow"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Login

    create_database(app)
    add_data(app)


    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    
    

def add_data(app):
    from .models import Login, Faculty, Student, Major, Subject, StudyPlan, TranScript, EnrollResult  
    with app.app_context():
                
        # Add Subject
        
        n=[]
        f = open("subject.txt",encoding="utf-8")
        for i in f: 
            n.append(i)
        subject_num = len(n)
        subject_had = db.session.query(Subject).count()
        if subject_num != subject_had:
            for l in n: 
                x = l.split(",")
                if len(x) == 4:
                    subject_add = Subject(id=x[0], subject_name_th=x[1], subject_name_en=x[2], subject_credit=int(x[3]))
                    db.session.add(subject_add)
                    db.session.commit()

                else:
                    subject_add = Subject(id=x[0],subject_name_th=x[1], subject_name_en=x[2], subject_credit=int(x[3]), subject_prerequisite=x[4])
                    db.session.add(subject_add)
                    db.session.commit()
                    


        # Add Faculty

        faculty_num = db.session.query(Faculty).count()
        if faculty_num == 1:
            pass
        else:
            CIS = Faculty(id='24',faculty_name='College of interdisciplinary studies')
            db.session.add(CIS)
            db.session.commit()

        # Add Major

        major_num = db.session.query(Major).count()
        if major_num == 3 :
            pass
        else:
            DSI = Major(id="20182067117526", major_name = "Data Science and Innovation", faculty_id = "24")
            PPE = Major(id="25550051100164", major_name = "Philosophy, Politics and Economics", faculty_id = "24")
            ISS = Major(id="25520051102782", major_name = "Interdisciplinary Studies of Social Science", faculty_id = "24")
            objects = [DSI, PPE, ISS]
            db.session.add_all(objects)
            db.session.commit()
       
        # Add study plan

        plan_had = db.session.query(StudyPlan).count()
        plan_num = pd.read_csv('DSIstudyplan.csv')
        if plan_had != len(plan_num):
            for i in range(len(plan_num)):
                plan_add = StudyPlan(id=plan_num.iloc[i][0], plan=plan_num.iloc[i][1], study_plan_years=str(plan_num.iloc[i][2]), semester=plan_num.iloc[i][3], major_id=str(plan_num.iloc[i][4]))
                db.session.add(plan_add)
                db.session.commit()


