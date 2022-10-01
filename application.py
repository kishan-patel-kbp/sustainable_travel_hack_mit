from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    name = 'Kishan Bob'
    return render_template('index.html', title='Welcome', username=name)
