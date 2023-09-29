from flask import request, jsonify
from ..models.Channels import Channel  

class ChannelController:
    @staticmethod
    def create_channel():
        try:
            data = request.json
            nombre = data.get("nombre")
            servidor_id = data.get("servidor_id")

            if nombre is None or servidor_id is None:
                return jsonify({"error": "Se requieren nombre y servidor_id para crear un canal"}), 400  # Bad Request

            # Crea una instancia de la clase Channel y llama al método create_channel
            new_channel = Channel(nombre=nombre, servidor_id=servidor_id)
            canal_id = new_channel.create_channel()

            if canal_id is not None:
                response = {
                    "message": "Canal creado exitosamente",
                    "canal_id": canal_id
                }
                return jsonify(response), 201  # Created
            else:
                return jsonify({"error": "Error al crear el canal"}), 500  # Internal Server Error

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error
