from flask import jsonify, Blueprint

meals_detect_blueprint = Blueprint('meals_detect', __name__)

@meals_detect_blueprint.route('/api/json/v1/meals_detect/<kategori>', methods=['GET'])
def get_meals_detect(kategori):
    if kategori == 'Kentang':
        meals = [
            {
                "strMeal": "Beef and Mustard Pie",
                "strMealThumb": "https://www.themealdb.com/images/media/meals/sytuqu1511553755.jpg",
                "idMeal": "52874"
            },
            {
                "strMeal": "Beef and Oyster pie",
                "strMealThumb": "https://www.themealdb.com/images/media/meals/wrssvt1511556563.jpg",
                "idMeal": "52878"
            },
            {
                "strMeal": "Beef Asado",
                "strMealThumb": "https://www.themealdb.com/images/media/meals/pkopc31683207947.jpg",
                "idMeal": "53071"
            }
        ]
    elif kategori == 'Kembang Kol':
        meals = [
            {
                "strMeal": "Ayam Percik",
                "strMealThumb": "https://www.themealdb.com/images/media/meals/020z181619788503.jpg",
                "idMeal": "53050"
            }
        ]
    elif kategori == 'Dessert':
        meals = [
            {
                "strMeal": "Apam balik",
                "strMealThumb": "https://www.themealdb.com/images/media/meals/adxcbq1619787919.jpg",
                "idMeal": "53049"
            }
        ]
    else:
        return jsonify({"message": "Category not found"})

    return jsonify({"meals": meals})