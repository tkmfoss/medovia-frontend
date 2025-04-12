import os
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')

# Sample data for orders
ORDERS = [
    {"order_id": "#1023", "customer": "John Doe", "date": "2025-03-15", "status": "Completed", "total": "$120"},
    {"order_id": "#1024", "customer": "Jane Smith", "date": "2025-03-16", "status": "Pending", "total": "$80"},
    {"order_id": "#1025", "customer": "Alice Brown", "date": "2025-03-17", "status": "Completed", "total": "$95"},
    {"order_id": "#1026", "customer": "Mike Davis", "date": "2025-03-18", "status": "Pending", "total": "$60"}
]

# Sample data for inventory
inventory_data = [
    {"id": 1, "name": "Paracetamol", "desc": "Pain reliever", "batch": "A101", "expires": "2025-07-12", "stock": 2, "image": "/static/paracetamol.png"},
    {"id": 2, "name": "Cough Syrup", "desc": "For cold and cough", "batch": "B202", "expires": "2025-05-01", "stock": 0, "image": "/static/cough.png"},
    {"id": 3, "name": "Antibiotic", "desc": "Fights bacteria", "batch": "C303", "expires": "2026-01-30", "stock": 12, "image": "/static/antibiotic.png"},
    {"id": 4, "name": "Ibuprofen", "desc": "Pain and fever relief", "batch": "D404", "expires": "2025-09-15", "stock": 15, "image": "/static/ibuprofen.png"},
    {"id": 5, "name": "Vitamin C", "desc": "Boosts immunity", "batch": "E505", "expires": "2025-12-20", "stock": 8, "image": "/static/vitamin_c.png"},
    {"id": 6, "name": "Insulin", "desc": "For diabetes management", "batch": "F606", "expires": "2026-02-28", "stock": 5, "image": "/static/insulin.png"},
    {"id": 7, "name": "Aspirin", "desc": "Pain and inflammation relief", "batch": "G707", "expires": "2025-11-10", "stock": 0, "image": "/static/aspirin.png"},
    {"id": 8, "name": "Antihistamine", "desc": "For allergies", "batch": "H808", "expires": "2025-06-05", "stock": 3, "image": "/static/antihistamine.png"},
    {"id": 9, "name": "Loperamide", "desc": "Anti-diarrheal", "batch": "I909", "expires": "2025-04-30", "stock": 7, "image": "/static/loperamide.png"},
    {"id": 10, "name": "Omeprazole", "desc": "Acid reflux treatment", "batch": "J010", "expires": "2026-03-15", "stock": 10, "image": "/static/omeprazole.png"},
    {"id": 11, "name": "Diphenhydramine", "desc": "Antihistamine for sleep", "batch": "K111", "expires": "2025-08-22", "stock": 4, "image": "/static/diphenhydramine.png"},
    {"id": 12, "name": "Metformin", "desc": "For diabetes management", "batch": "L212", "expires": "2026-05-05", "stock": 18, "image": "/static/metformin.png"},
    {"id": 13, "name": "Amoxicillin", "desc": "Antibiotic", "batch": "M313", "expires": "2026-07-12", "stock": 20, "image": "/static/amoxicillin.png"},
    {"id": 14, "name": "Lisinopril", "desc": "Blood pressure medication", "batch": "N414", "expires": "2025-10-10", "stock": 9, "image": "/static/lisinopril.png"},
    {"id": 15, "name": "Simvastatin", "desc": "Cholesterol medication", "batch": "O515", "expires": "2025-12-01", "stock": 13, "image": "/static/simvastatin.png"}
]


@app.route('/')
def home():
    return render_template('dashboard.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    data = {
        "sales": {"value": 1200, "change": "+15.27%"},
        "orders": {"value": 236, "change": "+5.5%"},
        "customers": {"value": 800, "change": "+11.02%"},
        "profits": {"value": 12000, "change": "+7.5%"},
        "out_of_stock": [
            {
                "name": "Paracetamol Tablets IP",
                "desc": "FRIZIUM 550 - CIPLA",
                "batch": "F102",
                "expires": "12/12/25",
                "image": "static/medicine1.png"
            }
        ],
        "expiring_soon": [
            {
                "name": "Paracetamol Tablets IP",
                "desc": "FRIZIUM 550 - CIPLA",
                "batch": "F102",
                "expires": "12/12/25",
                "image": "static/medicine1.png"
            }
        ]
    }
    return jsonify(data)

# Orders
@app.route('/orders')
def orders_page():
    return render_template('orders.html')

@app.route('/api/orders')
def get_orders():
    return jsonify(ORDERS)

@app.route('/api/orders/chart-data')
def get_chart_data():
    chart_data = {
        "labels": [],
        "data": []
    }
    today = datetime.now()
    for i in range(7):
        date = (today - timedelta(days=6 - i)).strftime('%b %d')
        chart_data["labels"].append(date)
        chart_data["data"].append(20 + i * 5)  # Dummy values
    return jsonify(chart_data)

# Inventory
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/api/inventory')
def api_inventory():
    low_stock = [item for item in inventory_data if 0 < item["stock"] <= 5]
    out_of_stock = [item for item in inventory_data if item["stock"] == 0]
    
    return jsonify({
        "total": len(inventory_data),
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "items": inventory_data  # Include full inventory for search
    })


@app.route('/inventory/<int:item_id>')
def view_item(item_id):
    item = next((item for item in inventory_data if item['id'] == item_id), None)
    if not item:
        return "Item not found", 404
    return render_template('restock.html', item=item)

@app.route('/api/restock/<int:item_id>', methods=['POST'])
def api_restock_item(item_id):
    data = request.get_json()
    quantity = int(data.get("quantity", 0))
    for item in inventory_data:
        if item["id"] == item_id:
            item["stock"] += quantity
            return jsonify({"status": "success", "new_stock": item["stock"]})
    return jsonify({"status": "error", "message": "Item not found"}), 404

# @app.route('/restock/<int:medicine_id>', methods=['POST'])
# def restock_medicine(medicine_id):
#     # Your logic to update quantity
#     return jsonify({'success': True})


# Other pages
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/offers')
def offers():
    return render_template('offers.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')



if __name__ == '__main__':
    app.run(debug=True)
