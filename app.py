from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
# client = MongoClient("mongodb+srv://230979:JkWoWYfjLgBQho7k@cluster0.d4x4mgp.mongodb.net/")
client = MongoClient("mongodb://localhost:27017")
db = client["Medicine"]
collection = db["Details"]

# Your products
products = [
    {
        "id": 4,
        "name": "Azithromycin Tablets 250 mg",
        "category": "antibiotics",
        "price": 60.0,
        "image": "static/images/Picture4.png",
        "pack": "Pack of 5 Tablets"
    },
    {
        "id": 5,
        "name": "Aspirin Tablets 75 mg",
        "category": "painkillers",
        "price": 8.0,
        "image": "static/images/Picture4.png",
        "pack": "Pack of 14 Tablets"
    },
    {
        "id": 6,
        "name": "Ciprofloxacin Tablets 500 mg",
        "category": "antibiotics",
        "price": 65.0,
        "image": "static/images/Picture4.png",
        "pack": "Pack of 10 Tablets"
    },
    {
        "id": 7,
        "name": "Digital Thermometer",
        "category": "equipment",
        "price": 250.0,
        "image": "static/images/Picture4.png",
        "pack": "1 Unit"
    },
    {
        "id": 8,
        "name": "Blood Pressure Monitor",
        "category": "equipment",
        "price": 1200.0,
        "image": "static/images/Picture4.png",
        "pack": "1 Unit"
    }
]


# Insert only if collection is empty
if collection.count_documents({}) == 0:
    collection.insert_many(products)
    print("Products inserted successfully!")

# Home route
@app.route('/')
def home():
    return render_template('Find.html')

# API route
@app.route('/api/products')
def get_products():
    products = []
    for product in collection.find():
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
        products.append(product)
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)
