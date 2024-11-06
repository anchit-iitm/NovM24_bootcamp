from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

@app.route('/get')
def get():

    var1 = 'basic.html, and the /hello route'
    var2 = True
    var3 = 10
    return jsonify({'str':var1, 'bool':var2, 'int':var3})

@app.route('/post', methods=['POST'])
def post():
    return 'post is working'



if __name__ == "__main__":
    app.run()