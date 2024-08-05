from flask import Flask, render_template

app = Flask(__name__)




@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)

@app.route("/create_usuario")
def create_usuario():
    return render_template("create_usuario.html")


@app.route("/read_usuario")
def read_usuario():
    return render_template("read_usuario.html")


@app.route("/update_usuario")
def update_usuario():
    return render_template("update_usuario.html")


@app.route("/delete_usuario")
def delete_usuario():
    return render_template("delete_usuario.html")

