from flask_restful import Resource
from flask import jsonify, make_response

# methods=['GET']
# def hello_world():
#     return 'Hello, World!'

class helloworld(Resource):
    def post(self):
        return 'Hello, World!'
    

class test(Resource):
    def get(self):
        return make_response(jsonify({'message': 'GET request successful'}), 200)
    
    def post(self):
        return make_response(jsonify({'message': 'POST request successful'}), 200)
    
    def put(self, pathArg):
        return make_response(jsonify({'message': 'PUT request successful', 'variable_passed': pathArg}), 200)
    
    def delete(self):
        return make_response(jsonify({'message': 'DELETE request successful'}), 200)