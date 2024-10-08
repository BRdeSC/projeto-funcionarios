from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, DateField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from datetime import datetime


#Formulário de Login
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[
        DataRequired("O login é obrigatório."),
        Length(min=4, max=10, message="Login deve contar no mínimo 4 e máximo 10 caracteres.")
    ])

    senha = PasswordField('Senha', validators=[
        DataRequired("A senha é obrigatória."),
        Length(min=4, max=10, message="Senha deve contar no mínimo 4 e máximo 10 caracteres.")
    ])   

    submit = SubmitField('Logar') 


#Formulário cadastro de usuário
class CreateUsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired("O nome é obrigatório."),
        Length(max=100, min=3, message="O nome deve conter no mínimo 3 e no máximo 100 caracteres.")
    ])

    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])

    login = StringField('Login', validators=[
        DataRequired("O login é obrigatório."),
        Length(min=4, max=10, message="Login deve contar no mínimo 4 e máximo 10 caracteres.")
    ])

    senha = PasswordField('Senha', validators=[
        DataRequired("A senha é obrigatória."),
        Length(min=4, max=10, message="Senha deve contar no mínimo 4 e máximo 10 caracteres.")
    ])

    submit = SubmitField('Cadastrar')


#formulário edição de usuário
class EditUsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(max=100, message="O nome deve conter no máximo 100 caracteres.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])
    login = StringField('Login', validators=[
        DataRequired("O login é obrigatório."),
        Length(min=3, max=10, message="Login deve contar no mínimo 3 e máximo 10 caracteres.")
    ])

    senha = PasswordField('Senha', validators=[
        DataRequired("A senha é obrigatória."),
        Length(min=3, max=10, message="Senha deve contar no mínimo 3 e máximo 10 caracteres.")
    ])

    submit = SubmitField('Editar')

    #********************************************************************************************************
    #********************************************************************************************************

#Formulário cadastro de funcionário
class CreateFuncionarioForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired("O nome é obrigatório."),
        Length(max=100, min=3, message="O nome deve conter no mínimo 3 e no máximo 100 caracteres.")
    ])

    tipo_contrato = StringField('Tipo_contrato', validators=[
        DataRequired("O tipo de contrato é obrigatório."),
        Length(max=50, min=3, message="O tipo de contrato deve conter no mínimo 3 e no máximo 50 caracteres.")
    ])

    admissao = DateField('Data de Admissão', format='%Y-%m-%d', validators=[DataRequired()])
        


    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])

    cidade = StringField('Cidade', validators=[
        DataRequired("A cidade é obrigatório."),
        Length(min=3, max=100, message="Cidade deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    funcao = StringField('Funcao', validators=[
        DataRequired("A função é obrigatória."),
        Length(min=3, max=100, message="Função deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
        
    
    mes_ferias = StringField('Mes_ferias', validators=[
        DataRequired("O campo ferias é obrigatório."),
        Length(min=3, max=20, message="O Mes das ferias deve contar no mínimo 3 e máximo 20 caracteres.")
    ])

    ramal = StringField('Ramal', validators=[
        DataRequired("O ramal é obrigatório."),
        Length(min=3, max=20, message="O ramal deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    foto = FileField('Foto')

    submit = SubmitField('Cadastrar')

    def validate_admissao(self, field):
        if field.data > datetime.now().date():
            raise ValidationError("A data de admissão não pode ser no futuro.")
    
    def validate_data_nascimento(self, field):
        if field.data >= datetime.now().date():
            raise ValidationError("A data de nascimento deve ser uma data passada.")


#Formulário edição de funcionário
class EditFuncionarioForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired("O nome é obrigatório."),
        Length(max=100, min=3, message="O nome deve conter no mínimo 3 e no máximo 100 caracteres.")
    ])

    tipo_contrato = StringField('Tipo_contrato', validators=[
        DataRequired("O tipo de contrato é obrigatório."),
        Length(max=50, min=3, message="O tipo de contrato deve conter no mínimo 3 e no máximo 50 caracteres.")
    ])

    admissao = DateField('Data de Admissão', format='%Y-%m-%d', validators=[DataRequired()])

    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])

    cidade = StringField('Cidade', validators=[
        DataRequired("A cidade é obrigatório."),
        Length(min=3, max=100, message="Cidade deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    funcao = StringField('Funcao', validators=[
        DataRequired("A função é obrigatória."),
        Length(min=3, max=100, message="Função deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    
    mes_ferias = StringField('Mes_ferias', validators=[
        DataRequired("O campo ferias é obrigatório."),
        Length(min=3, max=20, message="O Mes das ferias deve contar no mínimo 3 e máximo 20 caracteres.")
    ])

    ramal = StringField('Ramal', validators=[
        DataRequired("O ramal é obrigatório."),
        Length(min=3, max=20, message="O ramal deve contar no mínimo 3 e máximo 100 caracteres.")
    ])

    foto = FileField('Foto')

    submit = SubmitField('Editar')