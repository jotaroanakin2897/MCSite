from flask_pymongo import MongoClient
from sqlalchemy import null

from mcsite import app
from flask import render_template, request, redirect, url_for, flash
from mcsite.dbmodel import User, Note
from mcsite import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from flask_login import login_user, current_user, logout_user, login_required

from mcsite.forms import RegistrationForm, LoginForm, NoteForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classifica')
def classifica():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.tecweb
    classifica=db.get_collection("scores").find()

    return render_template('classifica.html',classifica=classifica)

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_pwd =  generate_password_hash(form.password.data, method='sha256')

        try:
            new_user = User(public_id = str(uuid.uuid4()), username=form.username.data, email=form.email.data, password=hashed_pwd, admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account created!', 'success')
            return redirect(url_for('index'))
        except:
            flash(f'Account not created!', 'danger')
            return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username = form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            flash(f'Logged in!', 'success')
            return redirect(url_for('index'))

        if not user:
            flash(f'Username not exist!', 'danger')
            return redirect(url_for('index'))

        if not check_password_hash(user.password, form.password.data):
            flash(f'Password error!', 'danger')
            return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(401)
def custom_401(error):
    return render_template('index.html', title='Game',error=error)

@app.route("/single")
@login_required
def play():
    return render_template('game.html', title='Game')

@app.route("/quiz", methods=['POST'])
@login_required
def quiz():
    citta=request.args.get('citta')
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.tecweb
    query=db.get_collection("tecweb")
    domande=query.find({ "citta": citta })
    lista_domande = list(domande)
    domande_non_disponibili=False
    if(len(lista_domande)==0):
        domande_non_disponibili=True


    return render_template('quiz.html', title='Game',citta=citta,domande_non_disponibili=domande_non_disponibili)

@app.route("/PrecreaQuiz", methods=['POST'])
@login_required
def PrecreaQuiz():
    citta=request.args.get('citta')

    return render_template('Creaquiz.html', title='Game',citta=citta)

@app.route("/info", methods=['GET'])
def info():

    return render_template('info.html', title='Game')

@app.route("/CreaQuiz",  methods=["GET", "POST"])
@login_required
def CreaQuiz():
    citta=request.args.get('citta')
    domanda = request.form['domanda']
    numRisposte = request.form['numRisposte']
    risposte=[]
    for i in range(0,int(numRisposte)):
        json_risp={"text": request.form['risposta'+str(i)], "correct": request.form['check'+str(i)]}
        risposte.append(json_risp)

    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.tecweb
    query = db.get_collection("tecweb")
    citta = request.args.get('citta')
    domande = query.find({"citta": citta})


    domanda_completa={
        'question': domanda,
        'citta': citta,
        'answers': risposte
    }
    if(len(list(domande))<10):
        query.insert_one(domanda_completa)
    else:
        print("errore!")



    print(risposte)


    return render_template('quiz.html', title='Game',citta=citta)

@app.route("/quizStarted", methods=['POST'])
@login_required
def quizStarted():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.tecweb
    query=db.get_collection("tecweb")
    citta=request.args.get('citta')
    domande=query.find({ "citta": citta })
    lista_domande = list(domande)

    return render_template('quizStarted.html', title='Continua a giocare',lista_domande=lista_domande,citta=citta)

@app.route("/valutazione", methods=['GET','POST'])
@login_required
def valuta():
    replies=(request.form.getlist('check'))

    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.tecweb
    query=db.get_collection("tecweb")
    citta=request.args.get('citta')
    domande=query.find({ "citta": citta })
    lista_domande = list(domande)
    punteggio=0

    risultati=[]
    risposta_esatta=""

    for i, domanda in enumerate(lista_domande):
        for risposta in domanda['answers']:
            if(replies[i]==risposta['text'] and risposta['correct']==True):
                punteggio+=1
            if (risposta['correct'] == True):
                risposta_esatta= risposta['text']
        risultati.append((domanda['question'],replies[i],risposta_esatta))


    import time
    ts = time.time()
    import datetime
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

    user=current_user.username
    collection = db.scores
    collection.insert({ "user": user,
     "score": punteggio,
     "time": st,
     })
    return render_template('risultati.html', title='Game',risultati=risultati,punteggio=punteggio)





    
@app.route("/note/delete/<note_id>", methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).first()

    if not note:
        flash(f'Note Not exist!', 'danger')
        return redirect(url_for('note'))

    db.session.delete(note)
    db.session.commit()
    flash(f'Note Deleted!', 'success')
    return redirect(url_for('note'))

@app.route('/manifest')
def manifest():
    from flask import make_response
    res = make_response(render_template('manifest.json'), 200)
    res.headers["Content-Type"] = "text/cache-manifest"
    return res