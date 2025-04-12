import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')

# ---------------------------
# Sample Datasets
# ---------------------------

ORDERS = [
    {"order_id": "#1023", "customer": "John Doe", "date": "2025-03-15", "status": "Completed", "total": "$120"},
    {"order_id": "#1024", "customer": "Jane Smith", "date": "2025-03-16", "status": "Pending", "total": "$80"},
    {"order_id": "#1025", "customer": "Alice Brown", "date": "2025-03-17", "status": "Completed", "total": "$95"},
    {"order_id": "#1026", "customer": "Mike Davis", "date": "2025-03-18", "status": "Pending", "total": "$60"}
]

customer_data = [
    {"id": "C001", "name": "John Doe", "email": "johndoe@email.com", "phone": "+1234567890", "orders": 15, "last_purchase": "2025-03-10", "status": "Active"},
    {"id": "C002", "name": "Jane Smith", "email": "janesmith@email.com", "phone": "+0987654321", "orders": 8, "last_purchase": "2025-02-28", "status": "Inactive"},
    {"id": "C003", "name": "Alice Brown", "email": "alice@email.com", "phone": "+1122334455", "orders": 22, "last_purchase": "2025-03-15", "status": "Active"},
    {"id": "C004", "name": "Bob Johnson", "email": "bob@email.com", "phone": "+5566778899", "orders": 5, "last_purchase": "2025-01-20", "status": "Inactive"},
    {"id": "C005", "name": "Emily Davis", "email": "emily@email.com", "phone": "+2233445566", "orders": 12, "last_purchase": "2025-03-05", "status": "Active"},
    {"id": "C006", "name": "Michael Wilson", "email": "michael@email.com", "phone": "+6677889900", "orders": 18, "last_purchase": "2025-03-12", "status": "Active"},
    {"id": "C007", "name": "Sarah Taylor", "email": "sarah@email.com", "phone": "+1177889900", "orders": 3, "last_purchase": "2025-02-10", "status": "Pending"}
]

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

# ---------------------------
# Routes
# ---------------------------

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    expiring_soon = [
        item for item in inventory_data
        if datetime.strptime(item["expires"], "%Y-%m-%d") < datetime.now() + timedelta(days=30)
    ]
    out_of_stock = [item for item in inventory_data if item["stock"] == 0]

    return jsonify({
        "sales": {"value": 1200, "change": "+15.27%"},
        "orders": {"value": 236, "change": "+5.5%"},
        "customers": {"value": 800, "change": "+11.02%"},
        "profits": {"value": 12000, "change": "+7.5%"},
        "out_of_stock": out_of_stock,
        "expiring_soon": expiring_soon
    })

@app.route('/orders')
def orders_page():
    return render_template('orders.html')

@app.route('/api/orders')
def get_orders():
    return jsonify(ORDERS)

@app.route('/api/orders/chart-data')
def get_order_chart():
    today = datetime.now()
    labels, data = [], []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        labels.append(day.strftime('%b %d'))
        data.append(20 + i * 5)
    return jsonify({"labels": labels, "data": data})

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
        "items": inventory_data
    })

@app.route('/inventory/<int:item_id>')
def view_item(item_id):
    item = next((item for item in inventory_data if item["id"] == item_id), None)
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

@app.route('/customer')
def customer_page():
    return render_template('customer.html')

@app.route('/api/customers')
def get_customers():
    return jsonify(customer_data)

@app.route('/api/customers/chart-data')
def customer_chart_data():
    return jsonify({
        "labels": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        "data": [20, 35, 50, 40, 70, 90]
    })

@app.route('/api/customers/search')
def search_customers():
    query = request.args.get('q', '').lower()
    results = [
        c for c in customer_data
        if query in c["name"].lower() or query in c["email"].lower() or query in c["phone"]
    ]
    return jsonify(results)

# ---------------------------
# New Sales Routes
# ---------------------------

def get_total_sales():
    # In a real scenario, you would query the database for the total sales value
    return 150000  # Example total sales (₹)

def get_total_orders():
    # In a real scenario, you would query the database to count the total number of orders
    return 250  # Example total orders

def get_sales_breakdown():
    # In a real scenario, this data would be fetched from the database
    # Here we are creating dummy data for the sales breakdown
    return [
        {"product": "Aspirin", "quantity": 50, "revenue": 5000, "margin": 20},
        {"product": "Paracetamol", "quantity": 30, "revenue": 3000, "margin": 25},
        {"product": "Ibuprofen", "quantity": 70, "revenue": 7000, "margin": 18},
        {"product": "Cough Syrup", "quantity": 40, "revenue": 4000, "margin": 15},
        {"product": "Antibiotics", "quantity": 60, "revenue": 6000, "margin": 22},
    ]

@app.route('/sales')
def sales():
    # Fetch sales data from the database (using sample values for now)
    total_sales = get_total_sales()  # Total revenue from sales
    total_orders = get_total_orders()  # Number of orders
    
    # Calculate average order value
    if total_orders > 0:
        average_order_value = total_sales / total_orders
    else:
        average_order_value = 0

    # Get sales breakdown (product, quantity sold, revenue, profit margin)
    sales_breakdown = get_sales_breakdown()
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    data = [3200, 4500, 5000, 6100, 7200, 8000]

    # Pass the data to the template
    return render_template('sales.html', 
                       total_sales=total_sales, 
                       average_order_value=average_order_value, 
                       sales_breakdown=sales_breakdown,
                       chart_data={"labels": labels, "data": data})


    

# ---------------------------
# Other Pages
# ---------------------------
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/api/notification')
def get_notification():
    alerts = []
    for item in inventory_data:
        if item["stock"] == 0:
            alerts.append(f"{item['name']} is out of stock.")
        elif datetime.strptime(item["expires"], "%Y-%m-%d") < datetime.now() + timedelta(days=15):
            alerts.append(f"{item['name']} is expiring soon on {item['expires']}.")
    return jsonify(alerts)

@app.route('/offers')
def offers():
    return render_template('offers.html')

@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run(debug=True)
