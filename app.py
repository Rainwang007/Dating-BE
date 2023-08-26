from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  

jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix='/api/auth')