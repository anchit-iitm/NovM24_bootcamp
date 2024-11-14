from flask_restful import Resource
from flask import jsonify, make_response
from flask_security import auth_required, roles_accepted
# methods=['GET']
# def hello_world():
#     return 'Hello, World!'

class helloworld(Resource):
    def post(self):
        return 'Hello, World!'
    

class testing(Resource):
    def get(self):
        return make_response(jsonify({'message': 'GET request successful'}), 200)
    
    def post(self):
        return make_response(jsonify({'message': 'POST request successful'}), 200)
    
    def put(self, pathArg):
        return make_response(jsonify({'message': 'PUT request successful', 'variable_passed': pathArg}), 200)
    
    # def put(self):
    #     return make_response(jsonify({'message': 'PUT request successful'}), 200)

    def delete(self):
        return make_response(jsonify({'message': 'DELETE request successful'}), 200)
    

from flask import request
from models import db, test
class storeNew(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def post(self):
        form_data = request.get_json()
        var1 = form_data['var1FromRequest']
        var2 = form_data['var2FromRequest']
        var3 = form_data['var3FromRequest']
        # print('var1: ', var1, 'var2: ', var2, 'var3: ', var3)
        new_data = test(var1FromDb=var1, var2FromDb=var2, var3FromDb=var3)
        db.session.add(new_data)
        db.session.commit()
        return make_response(jsonify({'id': new_data.id, 'str':new_data.var1FromDb, 'bool':new_data.var2FromDb, 'int':new_data.var3FromDb}), 201)  
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def put(self):
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
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def delete(self):
        form_data = request.get_json()
        id = form_data['idFromJson']
        db_data = test.query.filter_by(id=id).first()
        if db_data:
            db.session.delete(db_data)
            db.session.commit()
            return make_response(jsonify({'id': db_data.id, 'str':db_data.var1FromDb, 'bool':db_data.var2FromDb, 'int':db_data.var3FromDb}), 202)
        else:
            return make_response(jsonify({'error': 'id not found'}), 404)

    @auth_required('token')  
    def get(self):
        from flask_security import current_user
        return make_response(jsonify({'message': 'GET request successful', 'email': current_user.email, 'role': current_user.roles[0].name, 'status': current_user.active}), 200)