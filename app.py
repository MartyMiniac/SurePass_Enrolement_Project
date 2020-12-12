from flask import Flask, request, jsonify
from flask_restx import Resource,Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from random import randrange
from mongoengine import connect, disconnect

from ORM.models import PanClient


app=Flask(__name__)
api=Api(app)
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)
db_uri='mongodb+srv://MartyMiniac:Qe12ws45@cluster0.niiit.mongodb.net/SurePass?retryWrites=true&w=majority'

#Exceptions declaration
class BackendError(Exception):
    def __init__(self, message='Backend Error'):
        super().__init__(message)

class ClientNotFound(Exception):
    def __init__(self, message='Pan not found'):
        super().__init__(message)

class ObjectIDNotFound(Exception):
    def __init__(self, message='Object ID not found in the Database'):
        super().__init__(message)

#GET : get the bearer authentication token
@app.route('/getAccessToken', methods=["GET"])
def token(): 
    secret = request.json.get('secret') 
    user_id = request.json.get('id')
    if secret == app.config['JWT_SECRET_KEY']:
        rsp={
            'bearer_token':create_access_token(identity = user_id)
        }
        return jsonify(rsp)
    else:
        return jsonify({'msg': 'Secret key incorrect'})

#GET : get the pan number details using pan number and bearer token
@api.route('/<pan>')
class Details(Resource):
    @jwt_required
    def get(self, pan):
        try:
            num = randrange(10)


            if num in (8,9):
                raise BackendError
            
            client=None

            connect(
                db='SurePass',
                host=db_uri
                )

            for clients in PanClient.objects:
                if clients.pan==pan:
                    client=clients
                    break
            
            #Exception for not able to find the client in the database
            if client is None:
                disconnect()
                raise ClientNotFound
            js={
                'pan': client.pan,
                'name': client.name,
                'dob': client.dob.strftime('%Y-%m-%d'),
                'father_name': client.father_name,
                'client_id': str(client.id)
            }
            disconnect()
            return js
        except Exception as e:
            return {'msg': str(e)}

#GET : get the pan number details using object id and bearer token
@api.route('/id/<id>')
class id(Resource):
    @jwt_required
    def get(self, id):
        try:
            client=None

            connect(
                db='SurePass',
                host=db_uri
                )

            for clients in PanClient.objects:
                if str(clients.id)==id:
                    client=clients
                    break
            
            #Exception for not able to find the object id in the database
            if client is None:
                disconnect()
                raise ObjectIDNotFound
            js={
                'pan': client.pan,
                'name': client.name,
                'dob': client.dob.strftime('%Y-%m-%d'),
                'father_name': client.father_name,
                'client_id': str(client.id)
            }
            disconnect()
            return js
        except Exception as e:
            return {'msg': str(e)}

if __name__ == '__main__':
    app.run(debug=True)