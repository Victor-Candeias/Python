from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from controllers.mongodb_handler import MongoDBHandler

# Renamed the Blueprint from '' to 'config_routes'
ui_app = Blueprint('app', __name__)
db_handler = MongoDBHandler("peripheral_device_manager", "device_manager")

# Route for displaying all items
@ui_app.route('/')
def index():
    items = db_handler.list_items()
    return render_template('index.html', items=items)

# Route for adding a new item (GET for form, POST for submission)
@ui_app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        db_handler.add_item({"name": name, "value": int(value)})
        return redirect(url_for('index.html'))
    return render_template('add_item.html')

# Route for updating an item
@ui_app.route('/update/<item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if request.method == 'POST':
        new_value = request.form['value']
        db_handler.update_item(item_id, {"value": int(new_value)})
        return redirect(url_for('index.html'))
    item = db_handler.get_item(item_id)
    return render_template('update_item.html', item=item)

# Route for deleting an item
@ui_app.route('/delete/<item_id>')
def delete_item(item_id):
    db_handler.delete_item(item_id)
    return redirect(url_for('index.html'))
