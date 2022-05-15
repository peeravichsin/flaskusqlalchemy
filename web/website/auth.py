from flask import Blueprint, session, abort, redirect, request,render_template,flash,url_for
from . import db
from .models import Login, Student
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
import pathlib
from os import path
import requests
from datetime import datetime

auth = Blueprint('auth', __name__)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "821661327953-jva1j149g2arqrsrovq1hum65tp9eui4.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://enrollcheck.westus3.cloudapp.azure.com/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@auth.route("/Glogin")
def Glogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["picture"] = id_info.get("picture")
    if '@dome.tu.ac.th' in session["email"] :
        user = Login.query.filter_by(id=session["google_id"]).first()
        if user:
            flash(f'Welcome { session["name"] }', category='success')
            return redirect("/auth_home")
        else:
            return redirect("/sign_up")
    elif '@dome.tu.ac.th' not in session['email']:
        flash('You are not allow to login', category='error')
        return redirect("/login")



@auth.route("/sign_up",methods =['GET','POST'])
def signup():
    if request.method == 'POST':
        user_id = session["google_id"]
        user_email = session["email"]
        student_email = session["email"]
        name = session["name"].split(' ')
        student_fname_en = name[0]
        student_lname_en = name[1]
        student_fname_th = request.form.get('student_fname_th')
        student_lname_th = request.form.get('student_lname_th')
        student_id = request.form.get('student_id')
        faculty_id = 24
        major_id = request.form.get('major_name')
        year = student_id[:2]
        current_time = datetime.now()
        study_year = str(int(str(int(current_time.year)+543)[2:4])-int(year))
        new_user =Login(id=user_id, email=user_email)
        db.session.add(new_user)
        db.session.commit()

        add_student = Student(id=student_id, student_fname_th=student_fname_th, student_lname_th=student_lname_th, student_fname_en=student_fname_en, student_lname_en=student_lname_en, student_email=student_email, login_id=user_id, major_id=major_id, faculty_id=faculty_id,study_year=study_year)
        db.session.add(add_student)
        db.session.commit()

        flash('Profile created!', category='success')
        return redirect('/auth_home')
        
    return render_template('sign_up.html')
   


@auth.route("/logout")
@login_is_required
def logout():
    session.clear()
    return redirect("/")

