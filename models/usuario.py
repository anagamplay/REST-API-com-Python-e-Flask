from sql_alchemy import banco
from flask import request, url_for

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
    
    def send_confirmation_email(self):
        link = request.url_root[:-1]  + url_for('userconfirm', user_id=self.user_id) 
        # slicing de strings
        request.url_root[:-1] # http://127.0.0.1:5000/  
        url_for('userconfirm', user_id=self.user_id) # /confimacao/{user_id}

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }
    
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    def save_user(slef):
        banco.session.add(slef)
        banco.session.commit()
    
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()