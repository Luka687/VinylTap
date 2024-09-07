from flask import Blueprint, jsonify, request
from models import db, User, Catalogue, CatalogueItem, Record
from jwt_handler import encode_jwt_token, encode_refresh_token, decode_refresh_token, token_required, admin_required

api = Blueprint('api', __name__)

@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@api.route("/records", methods = ["POST", "GET"])
@admin_required
def record_create():
    if request.method == "POST":      
        record = Record(
            name=request.args.get("name") or request.form.get("name"),
            genre=request.args.get("genre") or request.form.get("genre"))
        db.session.add(record)
        db.session.commit()
        return jsonify({"message": "Record created successfully", "record": record.name, "genre": record.genre}), 201
    
    if request.method == "GET":   
        records = Record.query.get().all()
        records_list = [{"id": record.id, "name": record.name, "genre": record.genre} for record in records]
        return jsonify({"records": records_list}), 200
    
@api.route("/records/<int:id>", methods = ["GET", "DELETE", "PATCH"])
@admin_required
def handle_record(id):
    record = Record.query.get(id)
    if record is None:
        return jsonify({
            'error': 'Record not found',
            'message': f'No record found with id {id}'
        }), 404
    
    if request.method == "GET":
        return jsonify({"message": "Record retrieved successfully", "record": record.name, "genre": record.genre}), 200
    
    if request.method == "DELETE":
        db.session.delete(record)
        db.session.commit()

        return jsonify({"message": "Record deleted successfully", "record": record.name, "genre": record.genre}), 200
    
    if request.method == "PATCH":
        record.name=request.args.get("name") or request.form.get("name")
        record.genre=request.args.get("genre") or request.form.get("genre")
        db.session.commit()
        return jsonify({"message": "Record edited successfully", "record": record.name, "genre": record.genre}), 200

#### USER RELATED FUNCTIONS ####
@api.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    } for user in users]), 200

@api.route('/users/<int:id>', methods=['GET'])
@admin_required
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({
            'error': 'User not found',
            'message': f'No user found with id {id}'
        }), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    }), 200

#### CATALOGUE RELATED FUNCTIONS ####
@api.route('/catalogues', methods=['POST', 'GET'])
@token_required
def handle_catalogues():
    if request.method == "POST": 
        user_id = request.user_id,
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        catalogue = Catalogue(
            user_id=user_id,
            name=request.args.get("name") or request.form.get("name")
        )
        db.session.add(catalogue)
        db.session.commit()
        return jsonify({"message": "Catalogue created successfully", "catalogue": catalogue.name, "user": catalogue.user_id}), 201
    
    if request.method == "GET":
        catalogues = Catalogue.query.all() 
        result = []
        for catalogue in catalogues:
            result.apend({
                'id': catalogue.id,
                'name': catalogue.name,
                'description': catalogue.description,
                'user_id': catalogue.user_id,
                'user_username': catalogue.user.username,  # Accessing the related User's username
                'catalogue_items': [
                    {
                        'user_id': item.user_id,
                        'record_id': item.record_id,
                        'catalogue_id': item.catalogue_id,
                        'record_name': item.record.name,  # Accessing the related Record's name
                        'record_genre': item.record.genre  # Accessing the related Record's genre
                    }
                    for item in catalogue.catalogue_items
                ]
            })
        return jsonify(result), 200

@api.route('/catalogues/<int:id>', methods=['GET', 'PATCH', 'DELETE',])
@token_required
def handle_catalogue(id):
    catalogue = Catalogue.query.get(id)
    if catalogue is None:
        return jsonify({'error': 'Catalogue not found'}), 404
    
    if request.method == 'GET':

        result = {
        'id': catalogue.id,
        'name': catalogue.name,
        'description': catalogue.description,
        'user_id': catalogue.user_id,
        'user_username': catalogue.user.username,
        'catalogue_items': [
            {
                'user_id': item.user_id,
                'record_id': item.record_id,
                'catalogue_id': item.catalogue_id,
                'record_name': item.record.name,
                'record_genre': item.record.genre
            }
            for item in catalogue.catalogue_items
        ]
    }
        
        return jsonify(result), 200
    
    if request.method == 'PATCH':
        catalogue.name = request.args.get("name") or request.form.get("name")  
        db.session.commit()
        return jsonify({"message": "Catalogue retrieved successfully", "catalogue": catalogue.name, "user": catalogue.user_id}), 200

    if request.method == 'DELETE':
        db.session.delete(catalogue)
        db.session.commit()
        return jsonify({'message': 'Catalogue deleted successfully', "catalogue": catalogue.name, "user": catalogue.user_id}), 200
    
#### CATALOGUE ITEM RELATED FUNCTIONS ####
@api.route('/catalogue_items', methods=['POST', 'GET'])
@token_required
def handle_catalogue_items():
    if request.method == 'POST':
        user_id = request.user_id
        record_id = request.args.get('record_id')
        catalogue_id = request.args.get('catalogue_id')

        # Validate that the user, record, and catalogue exist
        user = User.query.get(user_id)
        record = Record.query.get(record_id)
        catalogue = Catalogue.query.get(catalogue_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        if not catalogue:
            return jsonify({'error': 'Catalogue not found'}), 404

        # Create new catalogue item
        catalogue_item = CatalogueItem(
            user_id=user_id, 
            record_id=record_id, 
            catalogue_id=catalogue_id
            )
        db.session.add(catalogue_item)
        db.session.commit()

        return jsonify({
            'user_id': catalogue_item.user_id,
            'record_id': catalogue_item.record_id,
            'catalogue_id': catalogue_item.catalogue_id
        }), 201
    
    if request.method == 'GET':
        catalogue_items = CatalogueItem.query.all()
        return jsonify([{
            'user_id': item.user_id,
            'record_id': item.record_id,
            'catalogue_id': item.catalogue_id
        } for item in catalogue_items]), 200
    
@api.route('/catalogue_items/<int:user_id>/<int:record_id>/<int:catalogue_id>', methods=['GET', 'PATCH', 'DELETE'])
@token_required
def handle_catalogue_item(user_id, record_id, catalogue_id):
    catalogue_item = CatalogueItem.query.filter_by(user_id=user_id, record_id=record_id, catalogue_id=catalogue_id).first()
    if catalogue_item is None:
            return jsonify({'error': 'Catalogue item not found'}), 404

    if request.method == 'GET':
        
        return jsonify({
            'user_id': catalogue_item.user_id,
            'record_id': catalogue_item.record_id,
            'catalogue_id': catalogue_item.catalogue_id,
            'record_name': catalogue_item.record.name,
            'record_genre': catalogue_item.record.genre
        }), 200

    if request.method == 'PATCH':
        return jsonify({
            'user_id': catalogue_item.user_id,
            'record_id': catalogue_item.record_id,
            'catalogue_id': catalogue_item.catalogue_id,
            'record_name': catalogue_item.record.name,
            'record_genre': catalogue_item.record.genre
        }), 200

    if request.method == 'DELETE':       
        db.session.delete(catalogue_item)
        db.session.commit()

        return jsonify({'message': 'CatalogueItem deleted successfully'}), 200

#### AUTH RELATED FUNCTIONS  ####
@api.route("/register", methods = ["POST"])
def register():
    admin_str=request.args.get("is_admin") or request.form.get("is_admin")
    username=request.args.get("username") or request.form.get("username")
    password=request.args.get("password") or request.form.get("password")
    is_admin = admin_str.lower() == 'true'
    
    if not username or not username:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    user = User(username=username, is_admin = is_admin)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "User": user.username}), 201 

@api.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if not username or not password:
        return jsonify({"message": "Missing required parameters"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = encode_jwt_token(user.id, user.is_admin)
    refresh_token = encode_refresh_token(user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@api.route("/logout", methods=["POST"])
@token_required
def logout():
    return jsonify({"message": "Logout successful. Please remove the token from client storage."}), 200
     
@api.route("/refresh", methods=["GET"])
def refresh():
    refresh_token = request.args.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Refresh token is required"}), 400

    payload = decode_refresh_token(refresh_token)
    if "user_id" not in payload:
        return jsonify(payload), 403

    user_id = payload['user_id']
    new_access_token = encode_jwt_token(user_id)
    return jsonify({"access_token": new_access_token}), 200