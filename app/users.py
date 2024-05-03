from flask import Blueprint, request, jsonify
from app.models import User
from app.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt, current_user


userBP = Blueprint('users', __name__)


@userBP.route('/all')
@jwt_required()
def get_all_users():

    claims = get_jwt()

    if not claims.get('is_staff'): return jsonify({"error": "you dont have permission for that."}), 401

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    users = User.query.paginate(
        page = page,
        per_page = per_page
    )

    result = UserSchema().dump(users, many=True)

    return jsonify(
        {
            "users": result
        }
    ), 200


