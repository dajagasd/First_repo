import os
from forms import  AddForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

############################################

        # SQL DATABASE AND MODELS

##########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Manager(db.Model):

    __tablename__ = 'manager'
    id = db.Column(db.Integer,primary_key = True)
    Username= db.Column(db.Text)
    Password=db.Column(db.Text)
    Strength=db.Column(db.Text)

    def __init__(self,Username,Password,Strength):
        self.Username = Username
        self.Password = Password
        self.Strength = Strength
    def __repr__(self):
        return f"USER-NAME : {self.Username} PASSWORD : {self.Password} STRENGTH : {self.Strength}"

############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def Add_form():
    form = AddForm()

    if form.validate_on_submit():
        Username = form.Username.data
        Password = form.Password.data
        Strength = form.Strength.data

        # Add new Puppy to database
        new_pup = Manager(Username,Password,Strength)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('output'))

    return render_template('add.html',form=form)

@app.route('/list')
def output():
    # Grab a list of puppies from database.
    users = Manager.query.all()
    return render_template('output.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
