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

    from flask_cors import CORS
    CORS(init_app)

    from celery import Celery
    init_celery = Celery(init_app.import_name)
    # init_celery.conf.update(init_app.config) # the same class
    from config import celeryConfig
    init_celery.config_from_object(celeryConfig)

    from mailer import mailer
    mailer.init_app(init_app)

    from caching import cache
    cache.init_app(init_app)

    return init_app, init_api, init_celery

app, api, celery_app = create_app()
import celery_task

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'schedule-1': {
        'task': 'celery_task.helloWorld',
        'schedule': crontab(hour=11, minute=43)
    },
    'schedule-2': {
        'task': 'celery_task.add',
        'schedule': crontab(hour=11, minute=43),
        'args': (2, 4)
    },
    'schedule-3': {
        'task': 'celery_task.retrieve_data',
        'schedule': crontab(hour=11, minute=52),
        'args': (1,)
    }
}


@app.route('/helloworld') # /helloworld
def hello_world():
    return 'Hello, World!'

@app.route('/test_celery')
def test_celery():
    # result = celery_task.add.delay(3,6)
    # result = celery_task.retrieve_data.delay(3)
    result = celery_task.send_mail_to_all_users.delay()
    print(result)
    # while not result.ready():
    #     pass
    return {'task_id': result.id, 'task_result': result.get(), 'task_status': result.status}

from routes.test import helloworld, testing, storeNew
api.add_resource(helloworld, '/helloworld') # /api/helloworld
api.add_resource(testing, '/', '/<int:pathArg>') # /api/test
api.add_resource(storeNew, '/storeNew') # /api/storeNew

from routes.products import ProductResource, ProductSpecific
api.add_resource(ProductResource, '/product') # /api/products
api.add_resource(ProductSpecific, '/product/<int:id>') # /api/products/<id>

from routes.category import CategoryResource, CategorySpecific
api.add_resource(CategoryResource, '/category') # /api/category
api.add_resource(CategorySpecific, '/category/<int:id>') # /api/category/<id>


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
        return make_response(jsonify({'id': new_user.id, 'email':new_user.email, 'roles':new_user.roles[0].name, 'message': 'registration successful'}), 201)
    return make_response(jsonify({'email_provided': present_user.email, 'message':'user already exists'}), 409)


@app.route('/api/login', methods=['POST'])
def login_api():
    form_data = request.get_json()
    email_var = form_data['emailFromRequest']
    password_var = form_data['passwordFromRequest']
    # role_var = form_data['roleFromRequest'] # not needed
    present_user = user_datastore.find_user(email=email_var)
    if not present_user:
        return make_response(jsonify({'email': email_var, 'message':"email id is not registered with us"}), 404)
    if present_user.active == False:
        return make_response(jsonify({'email': email_var, 'message':"user is not active, please talk to admin"}), 401)
    if present_user.password == password_var:
        auth_token = present_user.get_auth_token()
        from flask_security import login_user
        login_user(present_user)
        db.session.commit()
        return make_response(jsonify({"authToken": auth_token,'email_provided': present_user.email, 'message':'user already exists and password is correct', 'role': present_user.roles[0].name}), 201)
    return make_response(jsonify({'email_provided': present_user.email, 'message':'password is incorrect'}), 401)



if __name__ == "__main__":
    app.run()