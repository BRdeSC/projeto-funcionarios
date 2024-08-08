from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    login = db.Column(db.String(10), unique=True, nullable=False)
    senha = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.nome}>'
    
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo_contrato = db.Column(db.String(50), nullable=False)
    admissao = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    funcao = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    mes_ferias = db.Column(db.String(20), nullable=False)
    ramal = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Funcionario {self.nome}>'