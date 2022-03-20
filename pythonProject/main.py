from flask import *
from flask_sqlalchemy import *
import flask_scss
from datetime import datetime
import os

app = Flask(__name__)
flask_scss.Scss(app)
if not os.path.exists('databases'):
    os.makedirs('databases')
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "databases/childrens.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
counter = 0


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String, primary_key=True)
    password = db.column(db.String)
    # children = db.relationship('Child', backref='users', lazy='True')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}:"


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.DateTime, default=datetime.now())
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    bmi = db.Column(db.String)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, birth_date, weight, height, bmi):
        self.name = name
        self.birth_date = birth_date
        self.weight = weight
        self.height = height
        self.bmi = bmi

    def _repr(self):
        return f"{self.name}:{self.birth_date}:{self.weight}:{self.height}:{self.bmi}"


"""
--------------------------------------
"""
def get_child_health( height,weight):
    bmi =  (weight / (height * height)) * 703

    if bmi < 18.5:
        return "Attention: Underweight"
    elif bmi <= 24.9:
        return "Normal"
    elif bmi <= 29.9:
        return "Attention: Overweight"
    else:
        return "Attention: Obese"




def create_note(name, birth_date, weight, height):
    health = get_child_health(height, weight)
    note = Child(name=name, birth_date=birth_date, weight=weight, height=height, bmi=health)
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)


def read_notes():
    return db.session.query(Child).all()


def update_note(note_id, text, done):
    db.session.query(Child).filter_by(id=note_id).update({
        "text": text,
        "done": True if done == "on" else False
    })
    db.session.commit()


def delete_note(note_id):
    db.session.query(Child).filter_by(id=note_id).delete()
    db.session.commit()


@app.route("/home", methods=["POST", "GET"])
def view_index():
    global counter
    counter += 1
    if request.method == "POST" and counter > 1:
        print('ok')
        create_note(request.form['name'],
                    datetime(int(request.form['birth_date'].split('-')[0]),
                             int(request.form['birth_date'].split('-')[1]),
                             int(request.form['birth_date'].split('-')[2])),
                    int(request.form['weight']),
                    int(request.form['height']))
    return render_template('home.html', notes=read_notes())


"""
--------------------------------------
"""


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.form.get('continue') == 'login':
            return redirect('/')
        else:
            pass

    with open('html/registration.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/', methods=['GET', 'POST'])
def app_html():
    with open('html/index.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    # text = request.form['firstname']
    # processed_text = f"<h2>hello, {text}</h2><button"
    # return processed_text
    if request.method == 'POST':
        if request.form.get('continue') == 'Continue':
            return redirect('home')
        elif request.form.get('continue') == 'register':
            return redirect('registration')
        else:
            pass
    elif request.method == 'GET':
        return render_template('html/home.html')
    with open('html/home.html', 'r') as html_content:
        return str(html_content.read())


@app.errorhandler(404)
def page_not_found(e):
    with open('html/404.html', 'r') as html_content:
        return str(html_content.read()), 404


db.create_all()
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        os.unlink(database_file)
        exit()
