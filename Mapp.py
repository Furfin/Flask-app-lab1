from flask import Flask,request,render_template
import  sqlite3

app = Flask(__name__)




@app.route('/')
def index():
    return 'Ok'



@app.route('/login/', methods=['GET', 'POST'])
def login():
    message = ""
    db = sqlite3.connect("flask.db")
    cur = db.cursor()
    cur.execute('select * from users;')
    
    message = ''

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data = cur.fetchall()
        for user in data:
            if username in user and password in user:
                message = 'correct credentials'
            else:
                message = 'try rentering your credentials'

    return render_template('login.html', message = message)


    



if __name__ == '__main__':
    app.run(debug=True)






