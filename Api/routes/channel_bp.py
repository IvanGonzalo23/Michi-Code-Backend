from flask import Blueprint, request, jsonify
from ..controllers.channel_controller import ChannelController

channel_bp = Blueprint('channel_bp', __name__)

channel_bp.route("/create_channel", methods=['POST'])(ChannelController.create_channel)