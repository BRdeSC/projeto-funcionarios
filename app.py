from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import pymysql # Para tratar exceções específicas
from forms import CreateUsuarioForm, EditUsuarioForm

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)

#**************** ROTAS USUARIO **********************************



@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)


#/: Rota para ler e exibir todos os usuários da tabela users.
@app.route("/read_usuario")
def read_usuario():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM usuario")
            usuarios = cur.fetchall()
        flash("Usuários listados com sucesso!", 'success')
        return render_template('read_usuario.html', usuarios=usuarios)
    except pymysql.MySQLError as e:
        flash(f"Erro ao conectar ao banco de dados: {e}", 'error')
        return render_template("read_usuario.html", usuarios=[])


#/add: Rota para adicionar um novo usuário à tabela usuario.
@app.route("/create_usuario", methods=['GET', 'POST'])
def create_usuario():

    form = CreateUsuarioForm()

    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        login_usuario = form.login.data
        senha_usuario = form.senha.data
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO usuario (nome_usuario, email_usuario, login_usuario, senha_usuario) VALUES (%s, %s, %s, %s)", (nome_usuario, email_usuario, login_usuario, senha_usuario))
                mysql.connection.commit()
            flash("Usuário adicionado com sucesso!", 'success')
            return redirect(url_for('read_usuario'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao adicionar usuário: {e}", 'error')       
    return render_template("create_usuario.html", form=form)


#/edit/<int:id>: Rota para editar um usuário existente.
@app.route('/edit/<int:id_usuario>', methods=['GET', 'POST'])
def edit_usuario(id_usuario):

    form = EditUsuarioForm()

    if request.method == 'POST' and form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        login_usuario = form.login.data
        senha_usuario = form.senha.data
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE usuario SET nome_usuario = %s, email_usuario = %s, login_usuario = %s, senha_usuario = %s WHERE id_usuario = %s", (nome_usuario, email_usuario, login_usuario, senha_usuario, id_usuario))
                mysql.connection.commit()
            flash("Usuário atualizado com sucesso!", 'success')
            return redirect(url_for('read_usuario'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao atualizar usuário: {e}", 'error')
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
            user = cur.fetchone()
        if user:
            form.nome.data = user[1]
            form.email.data = user[2]
            form.login.data = user[3]
            form.senha.data = user[4]
        else:
            flash("Usuário não encontrado!", 'error')
            return redirect(url_for('read_usuario'))
    except pymysql.MySQLError as e:
        flash(f"Erro ao recuperar dados do usuário: {e}", 'error')
        return redirect(url_for('read_usuario'))
    
    return render_template('update_usuario.html', form=form)
    

#/delete/<int:id>: Rota para excluir um usuário da tabela users.
@app.route('/delete/<int:id_usuario>', methods=['POST'])
def delete_usuario(id_usuario):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))    
            mysql.connection.commit()
        flash("Usuário excluído com sucesso!", 'success')
    except pymysql.MySQLError as e:
        flash(f"Erro ao excluir usuário: {e}", 'error')
    return redirect(url_for('read_usuario'))







#***************** ROTAS FUNCIONARIOS**************************
@app.route('/')
def home():
    return render_template("read_usuario.html")

@app.route("/create_funcionario")
def create_funcionario():
    return render_template("create_funcionario.html")


@app.route("/read_funcionarios")
def read_funcionarios():
    return render_template("read_funcionarios.html")


@app.route("/update_funcionario")
def update_funcionario():
    return render_template("update_funcionario.html")


@app.route("/delete_funcionario")
def delete_funcionario():
    return render_template("delete_funcionario.html")


@app.route("/navegacao")
def navegacao():
    return render_template("navegacao.html")


if __name__ == '__main__':
    app.run(debug=True)