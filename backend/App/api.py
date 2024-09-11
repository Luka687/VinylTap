from flask import Blueprint, jsonify, request
from models import db, User, Catalogue, CatalogueItem, Record, Rating
from jwt_handler import encode_jwt_token,token_required, admin_required

api = Blueprint('api', __name__)

@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@api.route("/records", methods = ["POST"])
@admin_required
def record_create():    
    record = Record(
        name=request.args.get("name") or request.form.get("name"),
        genre=request.args.get("genre") or request.form.get("genre"),
        year_of_release = request.args.get("year_of_release"),
        artist = request.args.get("artist"),
        img_link = request.args.get("img_link"),  
        rating = 0,
        num_of_rating = 0
        )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Record created successfully", "record": record.name, "genre": record.genre}), 201  
        
    
@api.route("/records", methods = ["GET"])
def record_get():
    records = Record.query.all()
    records_list = [{
        "id": record.id,
        "name": record.name, 
        "genre": record.genre,
        "artist": record.artist,
        "year_of_release": record.year_of_release,
        "rating": record.rating,
        "img_link":record.img_link
        } for record in records]
    return jsonify({"records": records_list}), 200

@api.route("/records/<int:id>", methods = ["DELETE", "PATCH"])
@admin_required
def handle_record(id):
    record = Record.query.get(id)
    if record is None:
        return jsonify({
            'error': 'Record not found',
            'message': f'No record found with id {id}'
        }), 404
    
    if request.method == "DELETE":
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted successfully", "record": record.name, "genre": record.genre}), 200
    
    if request.method == "PATCH":
        record.name=request.args.get("name") or request.form.get("name")
        record.genre=request.args.get("genre") or request.form.get("genre")
        record.year_of_release=request.args.get("year_of_release") or request.form.get("year_of_release")
        record.artist=request.args.get("artist") or request.form.get("artist")
        record.img_link=request.args.get("img_link") or request.form.get("img_link")

        db.session.commit()
        return jsonify({"message": "Record edited successfully", "record": record.name, "genre": record.genre}), 200
    
@api.route('/ratings/<int:user_id>/<int:record_id>', methods=['GET'])
def get_rating(user_id, record_id):
    rating = Rating.query.filter_by(user_id=user_id, record_id=record_id).first()
    
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404
    
    return jsonify({
        'record_id': rating.record_id,
        'user_id': rating.user_id,
        'rating': rating.rating,
    }), 200

@api.route('/ratings/<int:user_id>/<int:record_id>', methods=['POST', 'PATCH'])
@token_required
def create_rating(user_id, record_id):
    def add_rating(id, new_rating):
        record = Record.query.get(id)
        record.rating = ((int)(record.num_of_rating * record.rating) + (int)(new_rating))/(record.num_of_rating+1)
        record.num_of_rating+=1

    def subtract_rating(id, old_rating):
        record = Record.query.get(id)
        record.rating = ((int)(record.num_of_rating * record.rating) - old_rating)/(record.num_of_rating*1)
        record.num_of_rating-=1

    if request.method == 'POST':
        print('test')
        rating=request.args.get("rating")

        if not all([record_id, user_id, rating is not None]):
            return jsonify({'error': 'Record ID, User ID, and rating are required'}), 400
        
        existing_rating = Rating.query.filter_by(record_id=record_id, user_id=user_id).first()

        if existing_rating:
            return jsonify({'error': 'Rating already exists for this user and record'}), 409

        new_rating = Rating(record_id=record_id, user_id=user_id, rating=rating)
        db.session.add(new_rating)
        add_rating(record_id, new_rating.rating)
        db.session.commit()
        return jsonify({
            'record_id': new_rating.record_id,
            'user_id': new_rating.user_id,
            'rating': new_rating.rating,
        }), 201
    
    if request.method == 'PATCH':
        rating = Rating.query.filter_by(user_id=user_id, record_id=record_id).first()
        if not rating:
            return jsonify({'error': 'Rating not found'}), 404
        
        subtract_rating(record_id, rating.rating)
        rating.rating = request.args.get("rating")
        add_rating(record_id, (int)(request.args.get("rating")))

        db.session.commit()
        return jsonify({
            'record_id': rating.record_id,
            'user_id': rating.user_id,
            'rating': rating.rating,
        }), 200

@api.route('/ratings/<int:user_id><int:record_id>', methods=['DELETE'])
@token_required
def delete_rating(user_id, record_id):
    rating = Rating.query.filter_by(user_id=user_id, record_id=record_id).first()
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404

    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': 'Rating deleted successfully'}), 200
    
@api.route("/records/<int:id>", methods = ["GET"])
def get_record(id):
    record = Record.query.get(id)
    if record is None:
        return jsonify({
            'error': 'Record not found',
            'message': f'No record found with id {id}'
        }), 404
    return jsonify({
        "message": "Record retrieved successfully", 
        "id": record.id,
        "name": record.name, 
        "genre": record.genre,
        "artist": record.artist,
        "year_of_release": record.year_of_release,
        "rating": record.rating,
        "img_link":record.img_link
        }), 200

#### USER RELATED FUNCTIONS ####
@api.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
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
        catalogue.description = request.args.get("description") or request.form.get("description")   
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
    ##admin_str=request.args.get("is_admin") or request.form.get("is_admin")
    username=request.args.get("username") or request.form.get("username")
    password=request.args.get("password") or request.form.get("password")
    ##is_admin = admin_str.lower() == 'true'
    
    if not username or not username:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    user = User(username=username, is_admin = False)
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
    print(access_token)
    return jsonify({
        "token": access_token,
        'is_admin': user.is_admin,
        'user_id': user.id
    }), 200

@api.route("/logout", methods=["POST"])
@token_required
def logout():
    return jsonify({"message": "Logout successful. Please remove the token from client storage."}), 200