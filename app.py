from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = {}

@app.route('/')
def home():
    return jsonify({"message": "Inventory API is running. Use /inventory and /lookup/<barcode>"}), 200

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'barcode' not in data:
        return jsonify({"error": "barcode is required"}), 400
    barcode = data['barcode']
    if barcode in inventory:
        inventory[barcode]['quantity'] += data.get('quantity', 1)
    else:
        inventory[barcode] = {
            "barcode": barcode,
            "name": data.get('name', 'Unknown'),
            "brand": data.get('brand', 'Unknown'),
            "quantity": data.get('quantity', 1),
            "category": data.get('category', 'Not available')
        }
    return jsonify({"message": "Item added", "item": inventory[barcode]}), 201

@app.route('/inventory/<barcode>', methods=['DELETE'])
def delete_item(barcode):
    if barcode not in inventory:
        return jsonify({"error": "Item not found"}), 404
    del inventory[barcode]
    return '', 204

@app.route('/inventory/<barcode>', methods=['PUT'])
def update_item(barcode):
    if barcode not in inventory:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    if 'quantity' in data:
        inventory[barcode]['quantity'] = data['quantity']
    if 'name' in data:
        inventory[barcode]['name'] = data['name']
    return jsonify(inventory[barcode]), 200

@app.route('/lookup/<barcode>', methods=['GET'])
def lookup(barcode):
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        headers = {"User-Agent": "inventory-system/1.0 - Educational Project"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code!= 200:
            return jsonify({"error": "Product not found"}), 404
        data = response.json()
        if data.get('status') == 0:
            return jsonify({"error": "Product not found"}), 404
        product = data.get('product', {})
        result = {
            "barcode": barcode,
            "name": product.get('product_name', 'Unknown'),
            "brand": product.get('brands', 'Unknown'),
            "category": product.get('categories', 'Not available'),
            "image": product.get('image_url', '')
        }
        return jsonify(result), 200
    except Exception as e:
        print(f"LOOKUP ERROR: {e}")
        return jsonify({"error": f"Failed to fetch product: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)