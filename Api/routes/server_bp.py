from flask import Blueprint
from ..controllers.server_controller import ServerController


serverbp = Blueprint('server_bp', __name__)
serverbp.route("/inicio", methods=['POST'])(ServerController.create_server)
