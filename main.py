from flask import *
app = Flask(__name__)

@app.route('/home')
def homepage():
    with open('templates/home.html', 'r') as html_content:
        return str(html_content.read())


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.form.get('continue') == 'login':
            return redirect('/')
        else:
            pass

    with open('templates/registration.html', 'r') as html_content:
        return str(html_content.read())

@app.route('/list')
def list():
    with open('templates/list.html', 'r') as html_content:
        return str(html_content.read())

@app.route('/')
def app_html():
    with open('templates/index.html', 'r') as html_content:
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
        return render_template('login2.html')
    with open('templates/login2.html', 'r') as html_content:
        return str(html_content.read())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
