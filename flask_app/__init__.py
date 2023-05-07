from flask import Flask

server = Flask(__name__)
server.secret_key = "secret_key"