from flask_app import app
from flask import render_template, redirect, session, request, get_flashed_messages
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    results= User.get_email(request.form)
    session['user_id']= results['id']
    print(session['user_id'])
    return redirect('/dashboard')

#make dashboard route
#make a logout button

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_user_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
