# Filename: app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data store (in-memory)
items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = {
        'id': len(items) + 1,
        'name': data['name'],
        'description': data.get('description', '')
    }
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    data = request.get_json()
    item['name'] = data['name']
    item['description'] = data.get('description', item['description'])
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    # For development use; in production use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
