from flask import Flask,render_template,request,redirect,url_for
from dynamodb import dynamodb

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_survey',methods=['GET','POST'])
def create_survey():
    if request.method == 'POST':
        print(request.form)
        question = request.form['question']
        options = [opt.strip() for opt in request.form['options'].split(',')]
        
        response = dynamodb.put_item(
            TableName='survey',
            Item={
                'question':{'S':question},
                'options':{'L':[{'S':opt} for opt in options]}
            }
        )
        
        return redirect(url_for('home'))
    return render_template('create_survey.html')

if __name__ == '__main__':
    app.run(debug=True)