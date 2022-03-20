from flask import *
from flask_sqlalchemy import *
from datetime import datetime
import os

app = Flask(__name__)

if not os.path.exists('databases'):
    os.makedirs('databases')
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "databases/childrens.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

"""
--------------------------------------
"""


class Children(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)
    dateAdded = db.Column(db.DateTime, default=datetime.now())


def create_note(text):
    note = Children(text=text)
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)


def read_notes():
    return db.session.query(Children).all()


def update_note(note_id, text, done):
    db.session.query(Children).filter_by(id=note_id).update({
        "text": text,
        "done": True if done == "on" else False
    })
    db.session.commit()


def delete_note(note_id):
    db.session.query(Children).filter_by(id=note_id).delete()
    db.session.commit()


@app.route("/home", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_note(request.form['text'])
    with open('html\\home.html', 'r') as html_content:
        return str(html_content.read())


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

    with open('html\\registration.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/', methods=['GET', 'POST'])
def app_html():
    with open('html\\index.html', 'r') as html_content:
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
        return render_template('html\\home.html')
    with open('html\\home.html', 'r') as html_content:
        return str(html_content.read())


@app.errorhandler(404)
def page_not_found(e):
    with open('html\\404.html', 'r') as html_content:
        return str(html_content.read()), 404


if __name__ == '__main__':
    app.run(debug=True)
