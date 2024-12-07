from flask import abort, jsonify, request
from app import db
from app.views import blueprint
from app.models.users import User
from app.models.preference import Preference
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

@blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    if not request.json:
        abort(400, "Request must be in JSON format")

    # Validate the required fields
    def _validate() -> bool:
        return all(field in request.json for field in ["username", "email", "password"])

    if not _validate():
        abort(400, "One or more required fields are missing")

    _username = request.json['username']
    _email = request.json['email']
    _password = request.json['password']

    # Check if the user already exists
    exist_user = User.query.filter_by(email=_email).first()
    if exist_user:
        abort(400, 'User already exists')

    # Create a new user and hash the password
    new_user = User(
        username=_username,
        email=_email
    )
    new_user.set_password(_password)  # Hash and store the password
    db.session.add(new_user)
    db.session.commit()
    
    new_preference = Preference(
        user_id=new_user.id
    )
    db.session.add(new_preference)
    db.session.commit()

    return jsonify(new_user.serialize()), 201


@blueprint.route('/users', methods=['GET'])
def get_user_list():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@blueprint.route('/login', methods=["POST"])
def login():
    if not request.json:
        abort(400, "Request must be in JSON format")

    def _validate() -> bool:
        return all(field in request.json for field in ["username", "password"])

    if not _validate():
        abort(400, "One or more required fields are missing")

    _username = request.json['username']
    _password = request.json['password']

    # Check if user exists by username
    exist_user = User.query.filter_by(username=_username).first()
    if not exist_user:
        abort(401, "Invalid username")

    # Verify the password
    if not exist_user.check_password(_password):
        abort(401, "Invalid password")

    # Generate access and refresh tokens
    # If credentials are correct, create tokens with user ID as identity
    access_token = create_access_token(identity=str(exist_user.id))
    refresh_token = create_refresh_token(identity=str(exist_user.id))



    return jsonify(
        msg="Login successful",
        access_token=access_token,
        refresh_token=refresh_token
    ), 200
    

@blueprint.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def user_details(user_id):
    current_user_id = int(get_jwt_identity())

    
    # Check if the current user's ID matches the requested user ID
    if current_user_id != user_id:
        abort(403, "You are not authorized to view this user's details.")
    
    # Query the user by ID
    user = User.query.get(user_id)

    # If user does not exist, return a 404
    if not user:
        abort(404, "User not found")

    # Serialize the user data and return as JSON
    return jsonify(user.serialize()), 200


@blueprint.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    # Ensure we work with an integer if identity is stored as a string
    try:
        current_user_id = int(current_user_id)
    except ValueError:
        abort(401, "Invalid token identity")
        
    if not request.json:
        abort(400, 'Request must be in JSON format')
        
    def _validate() -> bool:
        required_fields = ["username", "email", "password"]
        # If none of the required fields are present, this returns True
        return not any(field in request.json for field in required_fields)
    
    # If _validate() is True, that means no fields were provided at all
    if _validate():
        abort(400, "All fields are missing")
        
    _username = request.json.get('username')
    _email = request.json.get('email')
    _password = request.json.get('password')
    
    existing_user = User.query.get(user_id)
    
    if not existing_user:
        abort(404, "User not found")
        
    if _username is not None:
        existing_user.username = _username
    if _email is not None:
        existing_user.email = _email
    if _password is not None:
        # Assuming User model has a set_password method for hashing
        existing_user.set_password(_password)
        
    db.session.commit()

    return jsonify(existing_user.serialize()), 200

@blueprint.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()

    # Ensure we work with an integer if identity is stored as a string
    try:
        current_user_id = int(current_user_id)
    except ValueError:
        abort(401, "Invalid token identity")
        
    if current_user_id != user_id:
        abort(403, "You are not authorized to delete this user.")

    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200