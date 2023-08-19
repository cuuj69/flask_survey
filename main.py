from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_login import LoginManager, login_user, login_required, logout_user
from tables.dynamodb import table_name
from tables.dynamodb import dynamodb
from dotenv import load_dotenv
from user import User
import os
import uuid

load_dotenv

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def generate_unique_id():
    return str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        User.create(email,password)
        flash('Registration successful. Please log in.','sucess')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash,password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.','danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html') 

@app.route('/create_survey',methods=['GET','POST'])
@login_required
def create_survey():
    if request.method == 'POST':
        print(request.form)
        # question = request.form['question'] 
        # options = [opt.strip() for opt in request.form['options'].split(',')]
        
        questions = request.form.getlist('question[]')
        options_list = request.form.getlist('options[]')
        
        for question, options_str in zip(questions,options_list):
            options =[opt.strip() for opt in options_str.split(',')]
    
            survey_id = generate_unique_id()
            metadata_item = {
                'PK':{'S':f'SURVEY#{survey_id}'},
                'SK': {'S':f'METADATA#{survey_id}'},
                'Question':{'S':question},
                'Options':{'L': [{'S':option} for option in options]}
            }
            dynamodb.put_item(TableName=table_name,Item=metadata_item)
            
        return redirect(url_for('home'))
    return render_template('create_survey.html')

@app.route('/submit_response',methods=['POST'])
def submit_response():
    if request.method == 'POST':
        response = request.form['response']
        question_number = request.form['question_number']

        response_id = generate_unique_id()
        response_item ={
            'PK':{'S': f'RESPONSE#{response_id}'},
            'SK':{'S'f'ANSWER#{question_number}'},
            'Response':{'S':response}
        }
        dynamodb.put_item(TableName=table_name,Item=response_item)
        
        return redirect(url_for('home'))
    return render_template('create_survey.html')

if __name__ == '__main__':
    app.run(debug=True)