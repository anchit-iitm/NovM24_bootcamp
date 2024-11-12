from flask import Flask, jsonify, make_response, request
from flask_security import Security, auth_required, roles_accepted, roles_required

from models import db, test, user_datastore

def create_app():
    init_app = Flask(__name__)
    # import config
    # init_app.config.from_object(config)

    from config import DevelopmentConfig
    init_app.config.from_object(DevelopmentConfig)

    db.init_app(init_app)

    Security(init_app, user_datastore)

    from flask_restful import Api
    init_api = Api(init_app, prefix='/api')

    return init_app, init_api

app, api = create_app()


@app.route('/helloworld') # /helloworld
def hello_world():
    return 'Hello, World!'

from routes.test import helloworld, test, storeNew
api.add_resource(helloworld, '/helloworld') # /api/helloworld
# api.add_resource(test, '/', '/<int:pathArg>') # /api/test
api.add_resource(storeNew, '/storeNew') # /api/storeNew


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
@auth_required('token')
@roles_accepted('admin', 'manager') # changed in day 3
def retrieve():
    idFromRequest = request.get_json()['idFromJson']
    db_data = test.query.filter_by(id=idFromRequest).first()
    var1 = db_data.var1FromDb
    var2 = db_data.var2FromDb
    var3 = db_data.var3FromDb
    return jsonify({'str':var1, 'bool':var2, 'int':var3})

@app.route('/retrieve/<int:idFromRequest>')
@auth_required('token')
@roles_accepted('admin', 'manager') # changed in day 3
def retrieveFromPath(idFromRequest):
    db_data = test.query.filter_by(id=idFromRequest).first()
    var1 = db_data.var1FromDb
    var2 = db_data.var2FromDb
    var3 = db_data.var3FromDb
    return jsonify({'str':var1, 'bool':var2, 'int':var3})


# http status codes
@app.route('/store', methods=['POST'])
@auth_required('token')
@roles_accepted('admin', 'manager') # admin or manager
# @roles_required('admin', 'manager') # admin and manager
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


# c = POST
# r = GET
# u = PUT
# d = DELETE

@app.route('/storeNew', methods=['POST', 'PUT', 'DELETE'])
def storeNew():
    if request.method == 'POST':
        form_data = request.get_json()
        var1 = form_data['var1FromRequest']
        var2 = form_data['var2FromRequest']
        var3 = form_data['var3FromRequest']
        # print('var1: ', var1, 'var2: ', var2, 'var3: ', var3)
        new_data = test(var1FromDb=var1, var2FromDb=var2, var3FromDb=var3)
        db.session.add(new_data)
        db.session.commit()
        return make_response(jsonify({'id': new_data.id, 'str':new_data.var1FromDb, 'bool':new_data.var2FromDb, 'int':new_data.var3FromDb}), 201)  
    if request.method == 'PUT':
        form_data = request.get_json()
        id = form_data['idFromJson']
        var1 = form_data['var1FromRequest']
        var2 = form_data['var2FromRequest']
        var3 = form_data['var3FromRequest']
        db_data = test.query.filter_by(id=id).first()
        if db_data:
            db_data.var1FromDb = var1
            db_data.var2FromDb = var2
            db_data.var3FromDb = var3
            db.session.commit()
            return make_response(jsonify({'id': db_data.id, 'str':db_data.var1FromDb, 'bool':db_data.var2FromDb, 'int':db_data.var3FromDb}), 202)
        else:
            return make_response(jsonify({'error': 'id not found'}), 404)
    if request.method == 'DELETE':
        form_data = request.get_json()
        id = form_data['idFromJson']
        db_data = test.query.filter_by(id=id).first()
        if db_data:
            db.session.delete(db_data)
            db.session.commit()
            return make_response(jsonify({'id': db_data.id, 'str':db_data.var1FromDb, 'bool':db_data.var2FromDb, 'int':db_data.var3FromDb}), 202)
        else:
            return make_response(jsonify({'error': 'id not found'}), 404)

# @app.route('/update', methods=['POST'])
# @app.route('/update', methods=['PATCH'])
@app.route('/update', methods=['PUT'])
def update():
    form_data = request.get_json()
    id = form_data['idFromJson']
    var1 = form_data['var1FromRequest']
    var2 = form_data['var2FromRequest']
    var3 = form_data['var3FromRequest']
    db_data = test.query.filter_by(id=id).first()
    if db_data:
        db_data.var1FromDb = var1
        db_data.var2FromDb = var2
        db_data.var3FromDb = var3
        db.session.commit()
        return jsonify({'id': db_data.id, 'str':db_data.var1FromDb, 'bool':db_data.var2FromDb, 'int':db_data.var3FromDb})
    else:
        return jsonify({'error': 'id not found'})

@app.route('/delete', methods=['DELETE'])
def delete():
    form_data = request.get_json()
    id = form_data['idFromJson']
    db_data = test.query.filter_by(id=id).first()
    if db_data:
        db.session.delete(db_data)
        db.session.commit()
        return jsonify({'id': db_data.id, 'str':db_data.var1FromDb, 'bool':db_data.var2FromDb, 'int':db_data.var3FromDb})
    else:
        return jsonify({'error': 'id not found'})



@app.route('/api/register', methods=['POST'])
def register_api():
    form_data = request.get_json()
    email_var = form_data['emailFromRequest']
    password_var = form_data['passwordFromRequest']
    role_var = form_data['roleFromRequest'] #its in a string format
    present_user = user_datastore.find_user(email=email_var)
    if not present_user:
        # new_user = user_datastore.create_user(email=email_var, password=password_var, roles=[role_var, role_var1], active=True)
        new_user = user_datastore.create_user(email=email_var, password=password_var)
        if role_var == "manager":
            user_datastore.add_role_to_user(new_user, role_var)
            user_datastore.deactivate_user(new_user)
        if role_var == "customer":
            user_datastore.add_role_to_user(new_user, role_var)
        # user_datastore.add_role_to_user(new_user, role_var1)
        db.session.commit()
        return make_response(jsonify({'id': new_user.id, 'email':new_user.email, 'roles':new_user.roles[0].name}), 201)
    return make_response(jsonify({'email_provided': present_user.email, 'message':'user already exists'}), 409)


@app.route('/api/login', methods=['POST'])
def login_api():
    form_data = request.get_json()
    email_var = form_data['emailFromRequest']
    password_var = form_data['passwordFromRequest']
    role_var = form_data['roleFromRequest']
    present_user = user_datastore.find_user(email=email_var)
    if not present_user:
        return make_response(jsonify({'email': email_var, 'message':"email id is not registered with us"}), 404)
    if present_user.active == False:
        return make_response(jsonify({'email': email_var, 'message':"user is not active, please talk to admin"}), 401)
    if present_user.password == password_var:
        auth_token = present_user.get_auth_token()
        return make_response(jsonify({"authToken": auth_token,'email_provided': present_user.email, 'message':'user already exists and password is correct'}), 200)
    return make_response(jsonify({'email_provided': present_user.email, 'message':'password is incorrect'}), 401)



if __name__ == "__main__":
    app.run()