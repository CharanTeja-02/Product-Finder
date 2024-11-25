import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#file paths
PRODUCTS_FILE = 'products_data.pkl'
USERS_FILE = 'user_data.pkl'

#loading data from file
def load_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {}

#saves data to pickle file
def save_data(file_path, data):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

#variables for data base(initialising)
products_db = load_data(PRODUCTS_FILE)
users_db = load_data(USERS_FILE)

#registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']  # user or owner
    store = data.get('store') if role == 'Owner' else None

    if username in users_db:
        return jsonify({"error": "Username already exists"}), 400

    users_db[username] = {'password': password, 'role': role, 'store': store}
    save_data(USERS_FILE, users_db)
    return jsonify({"message": "Registration successful"}), 201

#login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users_db.get(username)
    if user and user['password'] == password:
        return jsonify({"message": "Login successful", "role": user['role'], "store": user.get('store')}), 200
    return jsonify({"error": "Invalid username or password"}), 401

# Search products and return malls with store availability
@app.route('/search_product/<name>', methods=['GET'])
def search_product(name):
    product_info = products_db.get(name)
    if not product_info:
        return jsonify({"error": "Product not found"}), 404
    
    malls = {}
    for product in product_info:
        mall_name = product['mall']
        if mall_name not in malls:
            malls[mall_name] = {'available': False, 'stores': []}

        # Track availability of the mall and store
        mall_available = False
        store_info = {
            "store": product['store'],
            "floor": product['floor'],
            "available": product['available']
        }

        if product['available']:
            mall_available = True
            malls[mall_name]['available'] = True
        
        malls[mall_name]['stores'].append(store_info)

    # Return a dictionary with mall and store availability
    return jsonify(malls)

#add product by owners
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    username = data['username']
    product_name = data.get('name')
    mall = data.get('mall')
    floor = data.get('floor')
    available = data.get('available')

    user = users_db.get(username)
    if user['role'] != 'Owner':
        return jsonify({"error": "Access denied"}), 403

    store = user.get('store')
    if not store:
        return jsonify({"error": "Owner is not associated with any store"}), 400

    products_db.setdefault(product_name, []).append({
        "mall": mall,
        "floor": floor,
        "store": store,
        "available": available
    })
    save_data(PRODUCTS_FILE, products_db)
    return jsonify({"message": f"Product added successfully to store '{store}'"}), 201

#delete product by owners
@app.route('/delete_product/<name>', methods=['DELETE'])
def delete_product(name):
    data = request.get_json()
    username = data['username']

    user = users_db.get(username)
    if user['role'] != 'Owner':
        return jsonify({"error": "Access denied"}), 403

    if name in products_db:
        del products_db[name]
        save_data(PRODUCTS_FILE, products_db)
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"error": "Product not found"}), 404

#update product by owner
@app.route('/update_product', methods=['PUT'])
def update_product():
    data = request.get_json()
    username = data['username']
    product_name = data.get('name')
    available = data.get('available')

    user = users_db.get(username)
    if not user or user['role'] != 'Owner':
        return jsonify({"error": "Access denied"}), 403

    product = products_db.get(product_name)
    if not product:
        return jsonify({"error": "Product not found. Add the product first."}), 404

    # Update availability for all instances of the product
    for entry in product:
        entry['available'] = available

    save_data(PRODUCTS_FILE, products_db)
    return jsonify({"message": f"Product '{product_name}' availability updated to {'Available' if available else 'Not Available'}."}), 200


if __name__ == '__main__':
    app.run(debug=True)
