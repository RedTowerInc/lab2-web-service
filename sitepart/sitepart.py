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
    "parameters": [
        {
            "name": "sort",
            "in": "query",
            "type": "string",
            "enum": ["цена", "название"],
            "description": "Поле для сортировки (цена, название)"
        },
        {
            "name": "order",
            "in": "query",
            "type": "string",
            "enum": ["asc", "desc"],
            "description": "Порядок сортировки (asc - по возрастанию, desc - по убыванию)"
        },
        {
            "name": "type",
            "in": "query",
            "type": "string",
            "description": "Фильтр по типу комплектующего"
        },
        {
            "name": "manufacturer",
            "in": "query",
            "type": "string",
            "description": "Фильтр по производителю"
        }
    ],
    "responses": {
        "200": {
            "description": "Список комплектующих с учетом сортировки и фильтрации",
            "schema": {
                "type": "array",
                "items": {"type": "object"}
            }
        }
    }
})
def get_components():
    """Получение списка комплектующих с возможностью фильтрации и сортировки"""
    result = list(components.values())

    # Фильтрация по типу
    component_type = request.args.get("type")
    if component_type:
        result = [c for c in result if c["тип"].lower() == component_type.lower()]

    # Фильтрация по производителю
    manufacturer = request.args.get("manufacturer")
    if manufacturer:
        result = [c for c in result if c["производитель"].lower() == manufacturer.lower()]

    # Сортировка
    sort_by = request.args.get("sort")
    if sort_by in ["цена", "название"]:
        order = request.args.get("order", "asc").lower()
        reverse = order == "desc"
        result.sort(key=lambda x: x[sort_by], reverse=reverse)

    return jsonify(result)


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


@sitepart.route('/statistics', methods=['GET'])
@swag_from({
    "responses": {
        "200": {
            "description": "Средняя, максимальная и минимальная цена комплектующих",
            "schema": {
                "type": "object",
                "properties": {
                    "средняя цена": {"type": "number"},
                    "максимальная цена": {"type": "number"},
                    "минимальная цена": {"type": "number"}
                }
            }
        }
    }
})
def get_statistics():
    """Вычисление средней, максимальной и минимальной цены"""
    if not components:
        return jsonify({"ошибка": "Нет данных"}), 404

    цены = [item["цена"] for item in components.values()]
    statistics = {
        "средняя цена": sum(цены) / len(цены),
        "максимальная цена": max(цены),
        "минимальная цена": min(цены)
    }
    return jsonify(statistics)
