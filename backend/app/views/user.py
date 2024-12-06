from flask import abort, jsonify, request
from app import db
from app.views import blueprint
from app.models.users import User
from flask_jwt_extended import create_access_token, create_refresh_token

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
    access_token = create_access_token(identity=_username)
    refresh_token = create_refresh_token(identity=_username)

    return jsonify(
        msg="Login successful",
        access_token=access_token,
        refresh_token=refresh_token
    ), 200
    

@blueprint.route('/users/<int:user_id>', methods=['GET'])
def user_details(user_id):
    # Query the user by ID
    user = User.query.get(user_id)

    # If user does not exist, return a 404
    if not user:
        abort(404, "User not found")

    # Serialize the user data and return as JSON
    return jsonify(user.serialize()), 200