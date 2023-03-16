import enum
import hashlib
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from flask_jwt_extended import jwt_required, create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_SECRET_KEY"] = "JwBGj2B4XFAKhYmn8Pgk0vH2w7UvgYfXAJ32e5rs8vI="

app_context = app.app_context()
app_context.push()

db = SQLAlchemy()
cors = CORS(app)
api = Api(app)
jwt = JWTManager(app)

class RolType(enum.Enum):
    ADMINISTRADOR = 1
    VENDEDOR = 2
    REPARTIDOR = 3
    CONTADOR = 4
    ALMACENISTA = 5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    rol = db.Column(db.String(3))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        id = fields.String()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

db.init_app(app)
db.create_all()

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        posts = User.query.all()
        return users_schema.dump(posts)
    def post(self):
        contrasena_encriptada = hashlib.md5(
                    request.json["password"].encode('utf-8')).hexdigest()
        new_user = User(
            username=request.json['username'],
            password=contrasena_encriptada,
            rol=request.json['rol'],
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    
class UserLogIn(Resource):
    def post(self):
        contrasena_encriptada = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest()
        usuario = User.query.filter(User.username == request.json["username"],
                                       User.password == contrasena_encriptada).first()
        db.session.commit()
        token_de_acceso = create_access_token(identity=usuario.id)
        return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "rol": usuario.rol}

api.add_resource(UserListResource, '/cpp/users')
api.add_resource(UserResource, '/cpp/users/<int:user_id>')
api.add_resource(UserLogIn, '/cpp/logIn')

if __name__ == '__main__':
    app.run(debug=True, host='localhost',port=5000)