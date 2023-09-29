from flask import Blueprint
from ..models.exceptions import BadRequest, NotFound, Forbidden, ServerError

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(400)
def handle_bad_request(error):
    error = BadRequest("Error en la operacion")
    return error.get_response()


@errors.app_errorhandler(404)
def handle_not_found(error):
    error = NotFound("Direccion no encontrada :( )")
    return error.get_response()

@errors.app_errorhandler(403)
def handle_forbidden(error):
    error = Forbidden("Acceso restringido")
    return error.get_response()

@errors.app_errorhandler(500)
def handle_server_error(error):
    error = ServerError("Error inesperado en el servidor D:")
    return error.get_response()