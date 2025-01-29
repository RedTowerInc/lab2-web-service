from flask import Blueprint, jsonify, request
from flasgger import swag_from

sitepart = Blueprint("sitepart", __name__)

# Хранилище данных в памяти (словарь)
components = {
    1: {"тип": "видеокарта", "название": "GeForce RTX 4080", "производитель": "NVIDIA", "цена": 150000},
    2: {"тип": "процессор", "название": "Ryzen 7 5800X", "производитель": "AMD", "цена": 30000},
    3: {"тип": "оперативная память", "название": "Kingston Fury 16GB", "производитель": "Kingston", "цена": 7000},
    4: {"тип": "SSD", "название": "Samsung 970 EVO 1TB", "производитель": "Samsung", "цена": 12000},
    5: {"тип": "материнская плата", "название": "ASUS ROG Strix B550-F", "производитель": "ASUS", "цена": 15000},
}

# Генерация нового ID
next_id = len(components) + 1


@sitepart.route('/components', methods=['GET'])
@swag_from({
    "responses": {
        "200": {
            "description": "Список всех комплектующих",
            "schema": {
                "type": "array",
                "items": {"type": "object"}
            }
        }
    }
})
def get_components():
    """Получение списка комплектующих"""
    return jsonify(components)


@sitepart.route('/components', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "тип": {"type": "string"},
                    "название": {"type": "string"},
                    "производитель": {"type": "string"},
                    "цена": {"type": "integer"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Комплектующее добавлено"},
        "400": {"description": "Ошибка валидации"}
    }
})
def add_component():
    """Добавление нового комплектующего"""
    global next_id
    data = request.json

    # Проверяем, что все нужные поля присутствуют
    if not all(key in data for key in ["тип", "название", "производитель", "цена"]):
        return jsonify({"ошибка": "Не все поля заполнены"}), 400

    components[next_id] = data
    next_id += 1
    return jsonify({"сообщение": "Комплектующее добавлено", "id": next_id - 1}), 201


@sitepart.route('/components/<int:item_id>', methods=['PUT'])
@swag_from({
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "type": "integer",
            "required": True
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "тип": {"type": "string"},
                    "название": {"type": "string"},
                    "производитель": {"type": "string"},
                    "цена": {"type": "integer"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Комплектующее обновлено"},
        "404": {"description": "Комплектующее не найдено"}
    }
})
def update_component(item_id):
    """Обновление комплектующего по ID"""
    if item_id not in components:
        return jsonify({"ошибка": "Комплектующее не найдено"}), 404

    data = request.json
    components[item_id] = data
    return jsonify({"сообщение": "Комплектующее обновлено"}), 200


@sitepart.route('/components/<int:item_id>', methods=['DELETE'])
@swag_from({
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        "200": {"description": "Комплектующее удалено"},
        "404": {"description": "Комплектующее не найдено"}
    }
})
def delete_component(item_id):
    """Удаление комплектующего по ID"""
    if item_id not in components:
        return jsonify({"ошибка": "Комплектующее не найдено"}), 404

    del components[item_id]
    return jsonify({"сообщение": "Комплектующее удалено"}), 200
