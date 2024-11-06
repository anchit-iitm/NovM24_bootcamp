from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite3'

db = SQLAlchemy(app)

class test(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True)
    var1FromDb = db.Column(db.String())
    var2FromDb = db.Column(db.Boolean)
    var3FromDb = db.Column(db.Integer)

with app.app_context():
    db.create_all()


@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

@app.route('/get')
def get():
    var1 = 'basic.html, and the /hello route'
    var2 = True
    var3 = 10
    return jsonify({'str':var1, 'bool':var2, 'int':var3})

# http status codes
@app.route('/postForm', methods=['POST'])
def postForm():
    form_data = request.form
    var1 = form_data['var1FromRequest']
    var2 = form_data['var2FromRequest']
    var3 = form_data['var3FromRequest']
    print('var1: ', var1, 'var2: ', var2, 'var3: ', var3)
    return 'post is working'

@app.route('/post', methods=['POST'])
def post():
    form_data = request.get_json()
    var1 = form_data['var1FromRequest']
    var2 = form_data['var2FromRequest']
    var3 = form_data['var3FromRequest']
    print('var1: ', var1, 'var2: ', var2, 'var3: ', var3)
    return 'post is working'


@app.route('/retrieve')
def retrieve():
    idFromRequest = request.get_json()['idFromJson']
    db_data = test.query.filter_by(id=idFromRequest).first()
    var1 = db_data.var1FromDb
    var2 = db_data.var2FromDb
    var3 = db_data.var3FromDb
    return jsonify({'str':var1, 'bool':var2, 'int':var3})

# http status codes
@app.route('/store', methods=['POST'])
def store():
    form_data = request.get_json()
    var1 = form_data['var1FromRequest']
    var2 = form_data['var2FromRequest']
    var3 = form_data['var3FromRequest']
    # print('var1: ', var1, 'var2: ', var2, 'var3: ', var3)
    new_data = test(var1FromDb=var1, var2FromDb=var2, var3FromDb=var3)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'id': new_data.id, 'str':new_data.var1FromDb, 'bool':new_data.var2FromDb, 'int':new_data.var3FromDb})

if __name__ == "__main__":
    app.run()