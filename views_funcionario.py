from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route("/create_funcionario")
def create_funcionario():
    return render_template("create_funcionario.html")


@app.route("/read_funcionarios")
def read_funcionarios():
    return render_template("read_funcionarios.html",
                           titulo = 'Lista de funcionários')


@app.route("/update_funcionario")
def update_funcionario():
    return render_template("update_funcionario.html")


@app.route("/delete_funcionario")
def delete_funcionario():
    return render_template("delete_funcionario.html")


@app.route("/navegacao")
def navegacao():
    return render_template("navegacao.html")