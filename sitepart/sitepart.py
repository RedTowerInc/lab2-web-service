from flask import Blueprint, jsonify, request
from flasgger import swag_from

sitepart = Blueprint("sitepart", __name__)

# Хранилище данных (словарь)
components = {
    1: {"тип": "видеокарта", "название": "GeForce RTX 4080", "производитель": "NVIDIA", "цена": 150000},
    2: {"тип": "процессор", "название": "Ryzen 7 5800X", "производитель": "AMD", "цена": 30000},
    3: {"тип": "оперативная память", "название": "Kingston Fury 16GB", "производитель": "Kingston", "цена": 7000},
    4: {"тип": "SSD", "название": "Samsung 970 EVO 1TB", "производитель": "Samsung", "цена": 12000},
    5: {"тип": "материнская плата", "название": "ASUS ROG Strix B550-F", "производитель": "ASUS", "цена": 15000},
}

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
