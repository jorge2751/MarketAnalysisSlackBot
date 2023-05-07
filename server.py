from flask_app import server
from flask_app.controllers import routes

if __name__=="__main__":     
    server.run(port=8080, debug=True)