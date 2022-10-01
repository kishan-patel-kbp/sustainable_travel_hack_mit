from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    name = 'Kishan Bob'
    return render_template('index.html', title='Fly Low', username=name)

if __name__ == '__main__':
    app.run(host='127.0.0.1')

