import os
from flask import Flask, render_template, request, jsonify, session, redirect, send_file
from werkzeug.utils import secure_filename
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

# New delivery dataset
delivery_data = [
    {"order_id": "#1034", "customer": "John Doe", "status": "Completed", "expected_date": "2025-03-15", "driver": "Mike Johnson"},
    {"order_id": "#1035", "customer": "Jane Smith", "status": "Pending", "expected_date": "2025-03-18", "driver": "Sarah Williams"},
    {"order_id": "#1036", "customer": "Robert Brown", "status": "Completed", "expected_date": "2025-03-14", "driver": "David Thompson"},
    {"order_id": "#1037", "customer": "Emma Davis", "status": "Failed", "expected_date": "2025-03-16", "driver": "Mike Johnson"},
    {"order_id": "#1038", "customer": "Michael Wilson", "status": "Completed", "expected_date": "2025-03-17", "driver": "Lisa Martinez"},
    {"order_id": "#1039", "customer": "Olivia Taylor", "status": "Pending", "expected_date": "2025-03-19", "driver": "David Thompson"},
    {"order_id": "#1040", "customer": "William Miller", "status": "Completed", "expected_date": "2025-03-15", "driver": "Sarah Williams"},
    {"order_id": "#1041", "customer": "Sophia Anderson", "status": "Completed", "expected_date": "2025-03-16", "driver": "Mike Johnson"},
    {"order_id": "#1042", "customer": "James Jackson", "status": "Failed", "expected_date": "2025-03-17", "driver": "Lisa Martinez"},
    {"order_id": "#1043", "customer": "Emily White", "status": "Pending", "expected_date": "2025-03-20", "driver": "David Thompson"}
]

# New offers dataset
offers_data = [
    {"id": 1, "name": "Summer Sale", "discount": 20, "expiry_date": "2025-06-30", "description": "Flat 20% off on all medicines.", "status": "Active"},
    {"id": 2, "name": "Festive Discount", "discount": 15, "expiry_date": "2025-04-15", "description": "Limited time 15% discount on selected items.", "status": "Expiring Soon"},
    {"id": 3, "name": "Health Pack Offer", "discount": 10, "expiry_date": "2025-05-20", "description": "10% discount on health supplement packs.", "status": "Active"},
    {"id": 4, "name": "Winter Special", "discount": 25, "expiry_date": "2025-02-28", "description": "25% off on winter health essentials.", "status": "Expired"}
]

# New notifications dataset
notifications_data = [
    {"id": 1, "type": "alert", "message": "Ibuprofen inventory is running low", "created_at": datetime.now() - timedelta(days=2), "is_unread": True, "icon": "🚨"},
    {"id": 2, "type": "promo", "message": "New Summer Sale promotion added", "created_at": datetime.now() - timedelta(days=1), "is_unread": True, "icon": "🎉"},
    {"id": 3, "type": "update", "message": "System maintenance scheduled for tonight", "created_at": datetime.now() - timedelta(hours=12), "is_unread": True, "icon": "📢"},
    {"id": 4, "type": "alert", "message": "Paracetamol stock is critically low", "created_at": datetime.now() - timedelta(hours=8), "is_unread": False, "icon": "🚨"},
    {"id": 5, "type": "update", "message": "Dashboard reports updated", "created_at": datetime.now() - timedelta(hours=5), "is_unread": True, "icon": "📢"},
    {"id": 6, "type": "promo", "message": "Flash sale starting in 2 hours", "created_at": datetime.now() - timedelta(hours=2), "is_unread": False, "icon": "🎉"},
    {"id": 7, "type": "alert", "message": "Cough Syrup is out of stock", "created_at": datetime.now() - timedelta(hours=1), "is_unread": True, "icon": "🚨"}
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
# Sales Routes
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
# Delivery Routes
# ---------------------------

@app.route('/delivery')
def delivery():
    # Get delivery statistics
    total_deliveries = len(delivery_data)
    completed_deliveries = sum(1 for d in delivery_data if d["status"] == "Completed")
    pending_deliveries = sum(1 for d in delivery_data if d["status"] == "Pending")
    failed_deliveries = sum(1 for d in delivery_data if d["status"] == "Failed")
    
    delivery_stats = {
        "total": total_deliveries,
        "completed": completed_deliveries,
        "pending": pending_deliveries,
        "failed": failed_deliveries
    }
    
    # Count notifications for the header
    notification_count = sum(1 for n in notifications_data if n["is_unread"])
    
    return render_template('delivery.html', 
                          delivery_stats=delivery_stats,
                          deliveries=delivery_data,
                          notification_count=notification_count)

@app.route('/api/delivery/chart-data')
def delivery_chart_data():
    # Get the last 7 days
    today = datetime.now()
    labels = []
    data = []
    
    # Create sample delivery data for last 7 days
    # In real app, would be from database
    for i in range(7):
        day = today - timedelta(days=6-i)
        labels.append(day.strftime('%b %d'))
        # Generate some random but consistent data
        data.append(30 + (i * 10) + (i % 3 * 5))
    
    return jsonify({
        "labels": labels,
        "data": data
    })

@app.route('/api/delivery')
def api_delivery():
    return jsonify(delivery_data)

# ---------------------------
# Offers Routes
# ---------------------------

@app.route('/offers')
def offers():
    # Update offer statuses based on expiry dates
    today = datetime.now().date()
    notification_count = sum(1 for n in notifications_data if n["is_unread"])
    
    for offer in offers_data:
        expiry = datetime.strptime(offer["expiry_date"], "%Y-%m-%d").date()
        if expiry < today:
            offer["status"] = "Expired"
        elif (expiry - today).days <= 15:
            offer["status"] = "Expiring Soon"
    
    active_offers = [offer for offer in offers_data if offer["status"] == "Active"]
    expiring_offers = [offer for offer in offers_data if offer["status"] == "Expiring Soon"]
    expired_offers = [offer for offer in offers_data if offer["status"] == "Expired"]
    
    return render_template('offers.html', 
                          active_offers=active_offers,
                          expiring_offers=expiring_offers,
                          expired_offers=expired_offers,
                          notification_count=notification_count)

@app.route('/api/offers')
def api_offers():
    return jsonify(offers_data)

@app.route('/api/offers/add', methods=['POST'])
def add_offer():
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ["name", "discount", "expiry_date", "description"]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # Create new offer ID
    new_id = max(offer["id"] for offer in offers_data) + 1
    
    # Determine status based on expiry date
    today = datetime.now().date()
    expiry = datetime.strptime(data["expiry_date"], "%Y-%m-%d").date()
    
    if expiry < today:
        status = "Expired"
    elif (expiry - today).days <= 15:
        status = "Expiring Soon"
    else:
        status = "Active"
    
    # Create new offer
    new_offer = {
        "id": new_id,
        "name": data["name"],
        "discount": data["discount"],
        "expiry_date": data["expiry_date"],
        "description": data["description"],
        "status": status
    }
    
    # Add to dataset
    offers_data.append(new_offer)
    
    return jsonify({"status": "success", "offer": new_offer})

# ---------------------------
# Notification Routes
# ---------------------------

def get_time_ago(notification_date):
    """Calculate time ago string for notifications"""
    now = datetime.now()
    delta = now - notification_date
    
    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"

@app.route('/notification')
def notification():
    # Count notifications by type
    alert_count = sum(1 for n in notifications_data if n["type"] == "alert")
    promo_count = sum(1 for n in notifications_data if n["type"] == "promo")
    update_count = sum(1 for n in notifications_data if n["type"] == "update")
    
    # Count unread notifications
    notification_count = sum(1 for n in notifications_data if n["is_unread"])
    
    # Format notifications for display
    notifications = []
    for n in notifications_data:
        notifications.append({
            "id": n["id"],
            "type": n["type"],
            "message": n["message"],
            "icon": n["icon"],
            "is_unread": n["is_unread"],
            "time_ago": get_time_ago(n["created_at"])
        })
    
    return render_template('notification.html',
                          notifications=notifications,
                          notification_count=notification_count,
                          alert_count=alert_count,
                          promo_count=promo_count,
                          update_count=update_count)

@app.route('/api/notification/count')
def get_notification_count():
    """Returns the count of unread notifications"""
    unread_count = sum(1 for n in notifications_data if n["is_unread"])
    return jsonify({"count": unread_count})

@app.route('/api/notification/categories')
def get_notification_categories():
    """Returns the count of notifications by category"""
    alert_count = sum(1 for n in notifications_data if n["type"] == "alert")
    promo_count = sum(1 for n in notifications_data if n["type"] == "promo")
    update_count = sum(1 for n in notifications_data if n["type"] == "update")
    
    return jsonify({
        "alert_count": alert_count,
        "promo_count": promo_count,
        "update_count": update_count
    })

@app.route('/api/notification/mark-read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    for notification in notifications_data:
        if notification["id"] == notification_id:
            notification["is_unread"] = False
            return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": "Notification not found"}), 404

@app.route('/api/notification/delete/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a notification"""
    global notifications_data
    
    initial_length = len(notifications_data)
    notifications_data = [n for n in notifications_data if n["id"] != notification_id]
    
    if len(notifications_data) < initial_length:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Notification not found"}), 404

@app.route('/api/notification/clear-all', methods=['DELETE'])
def clear_all_notifications():
    """Clear all notifications"""
    global notifications_data
    notifications_data = []
    return jsonify({"status": "success"})

@app.route('/api/notification/add', methods=['POST'])
def add_notification():
    """Add a new notification"""
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ["type", "message"]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # Set icon based on notification type
    icon = "📢"  # Default icon
    if data["type"] == "alert":
        icon = "🚨"
    elif data["type"] == "promo":
        icon = "🎉"
    
    # Create new notification ID
    new_id = 1
    if notifications_data:
        new_id = max(n["id"] for n in notifications_data) + 1
    
    # Create new notification
    new_notification = {
        "id": new_id,
        "type": data["type"],
        "message": data["message"],
        "created_at": datetime.now(),
        "is_unread": True,
        "icon": icon
    }
    
    # Add target field if provided
    if "target" in data:
        new_notification["target"] = data["target"]
    
    # Add to dataset
    notifications_data.append(new_notification)
    
    # Format for response
    response_notification = {
        "id": new_notification["id"],
        "type": new_notification["type"],
        "message": new_notification["message"],
        "icon": new_notification["icon"],
        "is_unread": new_notification["is_unread"],
        "time_ago": "just now"
    }
    
    return jsonify({"status": "success", "notification": response_notification})

# ---------------------------
# Other Pages
# ---------------------------

@app.route('/account')
def account():
    return render_template('account.html')

if __name__ == '__main__':
    app.run(debug=True)