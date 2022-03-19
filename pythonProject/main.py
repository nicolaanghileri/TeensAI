from flask import *
app = Flask(__name__)


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
