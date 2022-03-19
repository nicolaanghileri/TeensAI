from flask import *
from flask_sqlalchemy import *
from datetime import datetime
import os

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.column(db.Integer, primary_key=True, autoincrement=True)
    text = db.column(db.Text)
    done = db.column(db.Boolean)
    dateAdded = db.column(db.DateTime, default=datetime.now())


def create_note(text):
    note = Note(text=text)
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)


def read_notes():
    return db.session.query(Note).all()


def update_note(note_id, text, done):
    db.session.query(Note).filter_by(id=note_id).update(
        {
            "text": text,
            "done": True if "on" else False
        })
    db.session.commit()


def delete_note(note_id):
    db.session.query(Note).filter_by(id=note_id).delete()
    db.session.commit()


@app.route('/home')
def homepage():
    with open('home.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/')
def app_html():
    with open('login.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    # text = request.form['firstname']
    # processed_text = f"<h2>hello, {text}</h2><button"
    # return processed_text
    if request.method == 'POST':
        if request.form.get('continue') == 'Continue':
            return redirect('home')
        else:
            pass
    elif request.method == 'GET':
        return render_template('login2.html')
    with open('login2.html', 'r') as html_content:
        return str(html_content.read())


if __name__ == '__main__':
    app.run()
