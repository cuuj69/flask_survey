from flask import Flask,render_template,request,redirect,url_for
from dynamodb import dynamodb
from dynamodb import table_name
import uuid


app = Flask(__name__)


def generate_unique_id():
    return str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_survey',methods=['GET','POST'])
def create_survey():
    if request.method == 'POST':
        print(request.form)
        question = request.form['question']
        options = [opt.strip() for opt in request.form['options'].split(',')]

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