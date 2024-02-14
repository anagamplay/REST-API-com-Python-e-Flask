from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from blacklist import BLACKLIST
import traceback

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot left blank")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)
    
class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):
    # /cadatro
    def post(post):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400
        
        if UserModel.find_by_email(dados['email']):
            return {"message": "The email '{}' already exists.".format(dados['email'])}, 400

        if UserModel.find_by_login(dados['login']):
            return {'message': "The login '{}' already exists.".format(dados['login'])}
        
        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return{'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201
    
class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and compare_digest(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {'message': 'User not confirmed'}, 400
        return {'message': 'The Username or password is incorrect.'}, 401 # Unauthorized
    
class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifiers
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
    
class UserConfirm(Resource):
    # raiz_do_site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User id '{}' not found".format(user_id)}, 404
        
        user.ativado = True
        user.save_user()
        return {"message": "User id '{}' confirmed successfully".format(user_id)}, 200