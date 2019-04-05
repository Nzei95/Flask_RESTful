from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates a new endpoint /auth

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        '''
        for item in items:
            if item['name'] == name:
                return item
        '''
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item == None:
            return {'message': 'Item does not exist'}, 404
        else:
            return {'item' : item}, 200

    def post(self, name):
        '''
        data = request.get_json()
        item = {'name': name, 'price' : data['price']}
        items.append(item)
        return item, 201
        '''
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with that name '{}' already exists.".format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price' : data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'}

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug=True)