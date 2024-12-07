from flask import jsonify, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.views import blueprint
from app.models.users import User
from app.models.preference import Preference
from datetime import datetime

@blueprint.route('/get_preferences/<int:user_id>', methods=['GET'])
@jwt_required()
def get_preferences(user_id):
    current_user_id = get_jwt_identity()
    # If identity is stored as a string, convert it
    try:
        current_user_id = int(current_user_id)
    except ValueError:
        abort(401, "Invalid token identity")

    # Ensure the requesting user matches the requested user_id or handle authorization as needed
    if current_user_id != user_id:
        abort(403, "You are not authorized to view this user's preferences.")

    preference = Preference.query.filter_by(user_id=user_id).first()
    if not preference:
        abort(404, "User preferences not found")

    return jsonify(preference.serialize()), 200


@blueprint.route('/update_user_preferences/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_preferences(user_id):
    current_user_id = get_jwt_identity()
    # If identity is stored as string, convert to int
    try:
        current_user_id = int(current_user_id)
    except ValueError:
        abort(401, "Invalid token identity")

    if current_user_id != user_id:
        abort(403, "You are not authorized to update this user's preferences.")

    if not request.json:
        abort(400, "Request must be in JSON format")

    preference = Preference.query.filter_by(user_id=user_id).first()
    if not preference:
        # If no preference record exists, you may want to create one or return 404
        abort(404, "User preferences not found")

    # Extract fields from the JSON body
    theme = request.json.get("theme")
    language = request.json.get("language")
    notification_enabled = request.json.get("notification_enabled")

    # Update fields if they are provided
    if theme is not None:
        preference.theme = theme
    if language is not None:
        preference.language = language
    if notification_enabled is not None:
        preference.noticfication = notification_enabled

    # Update the updated_time (or updated_at) field to current time
    preference.updated_time = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Preferences updated successfully."}), 200
