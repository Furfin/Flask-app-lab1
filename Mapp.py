from flask import Flask,request,render_template,flash
import os

import  sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
loginMan = LoginManager(app)
loginMan.login_view = 'login'



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username

@loginMan.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    try:
        c_user = User.query.get(current_user.get_id())
    except:
        c_user =None
    return render_template('index.html',user = current_user,c_user=c_user)


@app.route('/defended')
@login_required
def defend():
    return render_template('index.html',user = current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message = ""
    
    message = ''
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        
            print(request.form)
            user = User.query.filter_by(username = request.form['username']).first()
            print(request.form['password'],user.password)
            user.set_password(user.password)
            

            if user is None or not user.check_password(request.form['password']):
                flash('invalid data')
                return render_template('login.html', message = '',user = current_user)
        
            login_user(user)
            print('auth')
            next_page = request.args.get('next')
            if not next_page:
                next_page = '/'
            return redirect(next_page)
            
    return render_template('login.html', message = '',user = current_user)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,password =form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form,user = current_user)


    



if __name__ == '__main__':
    app.run(debug=True)






