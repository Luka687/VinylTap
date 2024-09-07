from flask import Flask
from models import db
from api import api
from jwt_handler import encode_jwt_token, encode_refresh_token, decode_refresh_token, token_required, admin_required
import bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3300/vinyltap'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '0ff3b0d1cdb530c0d7de9fc5655fee0e0961d3cd9150c1aa05e4d7881be92185'
    app.config['REFRESH_SECRET_KEY'] = 'f2cd972adef8e38d619eb54aabf9b2879f9139fc0710d01eeeb61e11c516f4cf'
    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



