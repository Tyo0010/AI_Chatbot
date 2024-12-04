from flask import abort, jsonify, request
from app import db
from app.views import blueprint
from app.models.users import User

@blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    if not request.json:
        abort(400, "Request must be in JSON format")

    # Validate the required fields in the JSON request
    def _validate() -> bool:
        if "username" not in request.json:
            return False
        if "email" not in request.json:
            return False
        if "password" not in request.json:
            return False
        return True

    # If required fields are missing, return an error
    if not _validate():
        abort(400, "One or more required fields are missing")

    # Extract data from the JSON request
    _name = request.json['name']
    _email = request.json['email']
    _password = request.json['password']

    exist_user = User.query.filter_by(name=_name).first()
    
    # Check if the user already exists in the database
    if exist_user:
        abort(404, 'User already exists')


    output_path = f'photos/output/{_name}.png'  # Use an f-string here

    # Create a new user object
    new_user = User(
        name=_name,
        email=_email,
        password=_password
    )
    print(new_user.key)
    # Add the new user to the database and commit the changes
    db.session.add(new_user)
    db.session.commit()

    # Return the newly created racer as a JSON response
    return jsonify(new_user.serialize()), 201


@blueprint.route('/user_list', methods=['GET'])
def get_user_list():
    # Retrieve all users from the database
    users = User.query.all()
    
    # Serialize the list of user and return it as a JSON response
    serialized_users = [user.serialize() for user in users]

    # Return the list of users as a JSON response
    return jsonify(serialized_users)