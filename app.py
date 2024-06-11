from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

class UserResource(Resource):
    def get(self, user_id):

        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'User updated'})



class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        print('Fetched users from DB:', users_list)  # Add logging here
        return jsonify(users_list)

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        print('Added user to DB:', new_user)  # Add logging here
        return jsonify({'message': 'User created'})

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

@app.route('/')
def serve_home():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
