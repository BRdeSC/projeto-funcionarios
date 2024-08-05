from flask import Flask

app = Flask(__name__)


from views_usuario import *
from views_funcionario import *

if __name__ == '__main__':
    app.run(debug=True)