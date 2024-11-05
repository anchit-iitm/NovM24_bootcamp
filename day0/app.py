from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PORT'] = 2000

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    var1 = 'basic.html, and the /hello route'
    return render_template('basic.html', name=var1)

@app.route('/basic1', methods=['GET', 'POST'])
def basic1():
    if request.method == 'POST':
        var1 = request.form['nameFromHtml']
        return render_template('basic1.html', name=var1)
    if request.method == 'GET':
        var1 = 'Mahabodhi'
        return render_template('basic1.html', name=var1)


if __name__ == '__main__':
    app.run()