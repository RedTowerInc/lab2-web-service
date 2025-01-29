from flask import Blueprint, jsonify

sitepart = Blueprint("sitepart", __name__)


@sitepart.route('/components', methods=['GET'])
def get_components():
    """
    Получение списка комплектующих
    ---
    responses:
      200:
        description: Список комплектующих
    """
    components = [
        {"тип": "видеокарта", "название": "GeForce RTX 4080", "производитель": "NVIDIA", "цена": 150000},
        {"тип": "процессор", "название": "Ryzen 7 5800X", "производитель": "AMD", "цена": 30000},
    ]
    return jsonify(components)
