from flask import *
import random
import pyrebase  #29-dec

app = Flask(__name__)
app.secret_key = 'hastagp'


firebaseConfig = {     #29-dec
  "apiKey": "AIzaSyBcjMlz4izR7DKfE-ENm-Lnew4Kw2LAz0U",
  "authDomain": "questionhub-31462.firebaseapp.com",
  "databaseURL": "https://questionhub-31462-default-rtdb.firebaseio.com",
  "projectId": "questionhub-31462",
  "storageBucket": "questionhub-31462.appspot.com",
  "messagingSenderId": "595137055700",
  "appId": "1:595137055700:web:47bc19e153e4ec277a2441",
  "measurementId": "G-FTEHZ3647V"
}

firebase=pyrebase.initialize_app(firebaseConfig)
fdb=firebase.database()
fstorage = firebase.storage() #29-dec


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']
        
        data=fdb.child("users").child(username).get()
        if(data.val()):
            result=data.val()["password"]
            if password == result:
                qset=[]
                question=fdb.child("questions").get()
                for q in question.each():
                    if(q.key()!=0 and q.val()["answer"]=="Not Answered" ):
                        single=[q.key(),q.val()["questions"]]
                        qset.append(single)
                        

                return render_template('Home.html', values=qset, username=username)
            else:
                error="Incorrect Password"
        else:
            error = 'Username not registered'

    return render_template('login.html',error=error)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']

        data=fdb.child("users").child(username).get()

        if(data.val()):
            return render_template('Newacc.html',error="user Exists!!\nPlease Signin here")

        password = request.form['Password']
        phone = request.form['Phone']
        user_data={"password":password,"phone":phone}
        fdb.child("users").child(username).set(user_data)

        qset=[]
        question=fdb.child("questions").get()
        for q in question.each():
            if(q.key()!=0 and q.val()["answer"]=="Not Answered" ):
                single=[q.key(),q.val()["questions"]]
                qset.append(single)
                        

        return render_template('Home.html', values=qset, username=username)
    
@app.route('/Home')
def Home():
    qset=[]
    question=fdb.child("questions").get()
    for q in question.each():
        if(q.key()!=0 and q.val()["answer"]=="Not Answered" ):
            single=[q.key(),q.val()["questions"]]
            qset.append(single)
    
    return render_template('Home.html',values=qset)

    
@app.route('/answer', methods=['GET','POST'])
def answers():
    if request.method == 'POST':
        answer=request.form['answer']
        id=request.form['id']
        
        if not answer.isspace() and len(answer)!=0:
             fdb.child("questions").child(id).update({"answer":answer})

        return Home()

@app.route('/qlist', methods=['GET','POST'])
def qlist():
    if request.method=='POST':
        username = request.form['username']
        qset=[]
        question=fdb.child("questions").get()
        for data in question:
            if(data.key()==0):
                continue
            if(data.val().get("username")==username):
                single=[data.key(),data.val().get("questions")]
                qset.append(single)

    return render_template('MyQuestions.html', values = qset, username = username)
    
@app.route('/qinsert', methods=['GET' , 'POST'])
def qinsert():
    username = request.args.get('value')
    
    if request.method == 'POST':
        question = request.form['question']
        username = request.form['username']
        count = fdb.child("questionCount").get().val() or 0
        if (not question.isspace() and len(question)!=0):
            count += 1
            fdb.child("questionCount").set(count)
            ques={"questions":question,"answer":"Not Answered","username":username}
            fdb.child("questions").child(str(count)).set(ques)
        else:
            return render_template("Questions.html",error="Questions cannot contain only spaces!!")

        return Home()
    return Home()



@app.route('/Newacc.html')
def newacc():
    return render_template('Newacc.html')

@app.route('/Home.html')
def home():
    return render_template('Home.html')


@app.route('/MyQuestions.html')
def MyQuestions():
    return render_template('MyQuestions.html')

@app.route('/answer.html')
def answer():
    value = request.args.get('value')
    qset=[]
    question=fdb.child("questions").child(value).get()
    qset.append(value)
    qset.append(question.val().get('questions'))
    
    return render_template('answer.html', value=qset)

@app.route('/answerdisp.html')
def answerdisp():
    value = request.args.get('res')
    ans_set = []
    ans = fdb.child("questions").get()

    for i in ans.each():
        if (i.key() == int(value)):
            ans_set.extend([i.key(),i.val()["questions"],i.val()["answer"]])
    print(ans_set)
    return render_template('answerdisp.html', value=ans_set)

@app.route('/Questions.html')
def Questions():
    return render_template('Questions.html')

@app.route('/Profile.html')
def Profile():
    return render_template('Profile.html')




if __name__ == '__main__':
    app.run(debug=True, port=5050)
