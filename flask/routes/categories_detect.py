from flask import Blueprint, jsonify

categories_detect_blueprint = Blueprint('categories_detect', __name__)

@categories_detect_blueprint.route('/api/json/v1/categories_detect/<kategori>', methods=['GET'])
def get_categories_detect(kategori):
    requested_categories = kategori.split(',')

    response_data = {"categories": []}

    for category in requested_categories:
        if category == 'Kentang':
            data = {
                "idCategory": "1",
                "strCategory": "Kentang",
                "strCategoryThumb": "https://github.com/fadhilahmadd/rekomendasi-resep-dengan-deteksi-sayur-React-Native/blob/main/flask/img/kentang.png",
                "strCategoryDescription": "Beef is the culinary name for meat from cattle..."
            }
        elif category == 'Kembang Kol':
            data = {
                "idCategory": "2",
                "strCategory": "Kembang Kol",
                "strCategoryThumb": "https://www.themealdb.com/images/category/chicken.png",
                "strCategoryDescription": "Chicken is a type of domesticated fowl..."
            }
        elif category == 'Dessert':
            data = {
                "idCategory": "3",
                "strCategory": "Dessert",
                "strCategoryThumb": "https://www.themealdb.com/images/category/dessert.png",
                "strCategoryDescription": "Dessert is a course that concludes a meal..."
            }
        else:
            return jsonify({"message": f"Kategori '{category}' not found"}), 404

        response_data["categories"].append(data)

    return jsonify(response_data)
