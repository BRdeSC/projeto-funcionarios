from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config
import pymysql # Para tratar exceções específicas
from forms import CreateUsuarioForm, EditUsuarioForm, CreateFuncionarioForm, EditFuncionarioForm, LoginForm
from models import Usuario
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_login import login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)

# Configuração para upload de arquivos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static\\uploads')
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#**************************************************************************************************************************
#*****************ROTAS PARA LOGIN DE USUÁRIO******************************************************************************

@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        senha = form.senha.data
        try:
            usuario = Usuario.query.filter_by(login_usuario=login).first()
            if usuario and usuario.check_password(senha):
                login_user(usuario)
                flash("Login bem-sucedido!", 'success')
                return redirect(url_for('read_funcionario'))
            else:
                flash("Login ou senha incorretos.", 'error')
        except Exception as e:
            flash(f"Erro ao conectar ao banco de dados: {e}", 'error')
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado.", 'success')
    return redirect(url_for('login'))


@app.route("/protected")
@login_required
def protected():
    return "Você está em uma área protegida!"






#**************** INICIO ROTAS USUARIO ************************************************************************************
#**************************************************************************************************************************

@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)


#/: Rota para ler e exibir todos os usuários da tabela usuario.
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
    

#/delete/<int:id>: Rota para excluir um usuário da tabela usuario.
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



#***************** ROTAS FUNCIONARIOS**************************************************************************************
#**************************************************************************************************************************

#/: Rota para ler e exibir todos os funcionários da tabela funcionario.
@app.route("/read_funcionario")
def read_funcionario():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM funcionario")
            funcionarios = cur.fetchall()
        flash("Funcionarios listados com sucesso!", 'success')
        return render_template('read_funcionario.html', funcionarios=funcionarios)
    except pymysql.MySQLError as e:
        flash(f"Erro ao conectar ao banco de dados: {e}", 'error')
        return render_template("read_funcionario.html", funcionarios=[])



#/add: Rota para adicionar um novo funcionário à tabela funcionário.
@app.route("/create_funcionario", methods=['GET', 'POST'])
def create_funcionario():

    form = CreateFuncionarioForm()

    if form.validate_on_submit():
        nome = form.nome.data
        tipo_contrato = form.tipo_contrato.data
        admissao = form.admissao.data
        email = form.email.data
        cidade = form.cidade.data
        funcao = form.funcao.data
        data_nascimento = form.data_nascimento.data
        mes_ferias = form.mes_ferias.data
        ramal = form.ramal.data

        foto = form.foto.data
        print(foto)
        filename = None
        if foto and allowed_file(foto.filename):
            filename = email + "-" + secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO funcionario (nome, tipo_contrato, admissao, email, cidade, funcao, data_nascimento, mes_ferias, ramal, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, tipo_contrato, admissao, email, cidade, funcao, data_nascimento, mes_ferias, ramal, filename))
                mysql.connection.commit()
            flash("Funcionario adicionado com sucesso!", 'success')
            return redirect(url_for('read_funcionario'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao adicionar funcionario: {e}", 'error')       
    return render_template("create_funcionario.html", form=form)


#/edit/<int:id>: Rota para editar um funcionario existente.
@app.route('/edit_funcionario/<int:id>', methods=['GET', 'POST'])
def edit_funcionario(id):

    form = EditFuncionarioForm()

    if request.method == 'POST' and form.validate_on_submit():
        nome = form.nome.data
        tipo_contrato = form.tipo_contrato.data
        admissao = form.admissao.data
        email = form.email.data
        cidade = form.cidade.data
        funcao = form.funcao.data
        data_nascimento = form.data_nascimento.data
        mes_ferias = form.mes_ferias.data
        ramal = form.ramal.data

        foto = form.foto.data
        print(foto)
        filename = None
        if foto and allowed_file(foto.filename):
            filename = email + "-" + secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        try:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE funcionario SET nome = %s, tipo_contrato = %s, admissao = %s,email = %s, cidade = %s, funcao = %s, data_nascimento = %s, mes_ferias = %s, ramal = %s, foto = %s WHERE id = %s", (nome, tipo_contrato, admissao, email, cidade, funcao, data_nascimento, mes_ferias, ramal, filename, id))
                mysql.connection.commit()
            flash("Funcionário atualizado com sucesso!", 'success')
            return redirect(url_for('read_funcionario'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao atualizar funcionário: {e}", 'error')
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM funcionario WHERE id = %s", (id,))
            user = cur.fetchone()
        if user:
            form.nome.data = user[1]
            form.tipo_contrato.data = user[2]
            form.admissao.data = user[3]
            form.email.data = user[4]
            form.cidade.data = user[5]
            form.funcao.data = user[6]
            form.data_nascimento.data = user[7]
            form.mes_ferias.data = user[8]
            form.ramal.data = user[9]

            form.foto.data = user[10]

        else:
            flash("Funcionário não encontrado!", 'error')
            return redirect(url_for('read_funcionario'))
    except pymysql.MySQLError as e:
        flash(f"Erro ao recuperar dados do funcionario: {e}", 'error')
        return redirect(url_for('read_funcionaio'))
    
    return render_template('update_funcionario.html', form=form)


#rota para imagens

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def file_too_large(e):
    flash('O arquivo é muito grande. Tente um arquivo menor.', 'error')
    return redirect(request.url)




#/delete/<int:id>: Rota para excluir um funcionário da tabela funcionario.
@app.route('/delete_funcionario/<int:id>', methods=['POST'])
def delete_funcionario(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM funcionario WHERE id = %s", (id,))    
            mysql.connection.commit()
        flash("Funcionário excluído com sucesso!", 'success')
    except pymysql.MySQLError as e:
        flash(f"Erro ao excluir funcionário: {e}", 'error')
    return redirect(url_for('read_funcionario'))



#view_funcionario: Rota para lista apenas o funcionario que foi selecionado
@app.route("/funcionario/<int:id>")
def view_funcionario(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT *FROM funcionario WHERE id = %s", (id,))
            funcionario = cur.fetchone()
        if funcionario:
            return render_template("view_funcionario.html", funcionario=funcionario)
        else:
            flash("Funcionário não encontrado!" 'error')
            return redirect(url_for('read_funcionario'))
    except pymysql.MySQLError as e:
        flash(f"Erro ao recuperar dados do funcionário: {e}", 'error')
        return redirect(url_for('read_funcionario'))




if __name__ == '__main__':
    app.run(debug=True)