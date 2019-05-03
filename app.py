import os
import sqlite3
from flask import Flask, request, render_template, redirect, session, abort, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

_reg_no=''

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(15), unique=True)
    full_name = db.Column(db.String(15))
    email = db.Column(db.String(50))
    ad_year = db.Column(db.String(10))
    cur_session = db.Column(db.String(10))
    course = db.Column(db.String(10))
    year = db.Column(db.String(10))
    dep = db.Column(db.String(20))
    hall = db.Column(db.String(20))
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    reg_no = StringField('reg_no', validators=[InputRequired(), Length(min=4, max=15)], render_kw={'placeholder':'Registration number'})
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)], render_kw={'placeholder':'Password'})

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class TransaectionForm(FlaskForm):
    id = StringField('ID', validators=[InputRequired(), Length(max=10)], render_kw={'placeholder':'TRXID'})
    amount = StringField('Amount', validators=[InputRequired()], render_kw={'placeholder':'Transaction Amount'})
    acc_no = StringField('Mock Account No.', validators=[InputRequired(), Length(min=6, max=16)], render_kw={'placeholder':'Mock Acc No.'})
    pin = PasswordField('PIN', validators=[InputRequired(), Length(min=6, max=50)], render_kw={'placeholder':'4 Digit PIN'})



def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



@login_manager.user_loader
def loadUser(id):
    return User.query.get(int(id))

@app.route("/")
@login_required
def homePage():
    return redirect(url_for('user_page'))

@app.route('/user')
@login_required
def user_page():
    con = sqlite3.connect("database.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * from user where reg_no='" +session['_reg_no']+ "';")
    dic1 = cur.fetchone()
    cur.execute("select * from notification;")
    dic2 = cur.fetchall()
    return render_template('user.html', user=dic1, notifications=dic2)



@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(reg_no=form.reg_no.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                session['_reg_no'] = form.reg_no.data
                return redirect(url_for('homePage'))
        return '<h1>Invalid username/password</h1>'

    return render_template('login.html', form=form)


# depricated
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/transection_page', methods=['GET', 'POST'])
def transaction():
    form = TransaectionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('homePage'))
        return '<h1>Invalid username/password</h1>'

    return render_template('transection_page.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

    # alhamdulillah it works
