from flask import Flask, request

app = Flask(__name__)

# Temporary in-memory inventory
inventory = []

@app.route("/")
def home():
    return "Inventory Management System API is running!"

# READ: Get all items
@app.route("/items", methods=["GET"])
def get_items():
    return {"items": inventory}

# CREATE: Add a new item
@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    inventory.append(data)
    return {"message": "Item added", "item": data}, 201

# UPDATE: Modify an item by index
@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    if item_id < 0 or item_id >= len(inventory):
        return {"error": "Item not found"}, 404
    data = request.get_json()
    inventory[item_id].update(data)
    return {"message": "Item updated", "item": inventory[item_id]}

# DELETE: Remove an item by index
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id < 0 or item_id >= len(inventory):
        return {"error": "Item not found"}, 404
    removed = inventory.pop(item_id)
    return {"message": "Item deleted", "item": removed}

if __name__ == "__main__":
    # Bind to all interfaces so you can reach it from your browser
    app.run(host="0.0.0.0", port=5000, debug=True)
