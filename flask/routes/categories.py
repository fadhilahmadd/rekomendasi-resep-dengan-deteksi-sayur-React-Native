from flask import Blueprint, jsonify

categories_blueprint = Blueprint('categories', __name__)

@categories_blueprint.route('/api/json/v1/categories', methods=['GET'])
def get_categories():
    categories = [
        {
            "idCategory": "1",
            "strCategory": "Beef",
            "strCategoryThumb": "https://www.themealdb.com/images/category/beef.png",
            "strCategoryDescription": "Beef is the culinary name for meat from cattle..."
        },
        {
            "idCategory": "2",
            "strCategory": "Chicken",
            "strCategoryThumb": "https://www.themealdb.com/images/category/chicken.png",
            "strCategoryDescription": "Chicken is a type of domesticated fowl..."
        },
        {
            "idCategory": "3",
            "strCategory": "Dessert",
            "strCategoryThumb": "https://www.themealdb.com/images/category/dessert.png",
            "strCategoryDescription": "Dessert is a course that concludes a meal..."
        }
    ]
    return jsonify({"categories": categories})