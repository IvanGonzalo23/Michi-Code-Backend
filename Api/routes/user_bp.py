from flask import Blueprint,render_template
from ..controllers.user_controller import UserController


userbp = Blueprint('user_bp', __name__)
userbp.route("/createuser", methods=['POST'])(UserController.create_user)
userbp.route("/login", methods=['POST'])(UserController.login)
userbp.route("/<int:user_id>", methods=['PUT'])(UserController.edit_profile)
userbp.route("/<int:user_id>", methods=["DELETE"])(UserController.delete_user)