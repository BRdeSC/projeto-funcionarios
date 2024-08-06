from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

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
        Length(min=3, max=10, message="Login deve contar no mínimo 3 e máximo 10 caracteres.")
    ])

    senha = PasswordField('Senha', validators=[
        DataRequired("A senha é obrigatória."),
        Length(min=3, max=10, message="Senha deve contar no mínimo 3 e máximo 10 caracteres.")
    ])

    submit = SubmitField('Cadastrar')




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