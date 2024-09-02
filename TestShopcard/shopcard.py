# file: shopcard_api.py

import requests

BASE_URL = "http://localhost:5000/api/shopcard"

def get_shopcards():
    """Fetches all shop cards."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def post_shopcard(data):
    """Creates a new shop card.
    
    Args:
        data (dict): A dictionary containing the details of the shop card.
    
    Returns:
        dict: The response data from the API.
    """
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def delete_shopcard(txnKeyId):
    """Deletes a shop card by txnKeyId.
    
    Args:
        txnKeyId (str): The transaction key ID of the shop card to delete.
    
    Returns:
        dict: The response data from the API.
    """
    url = f"{BASE_URL}/{txnKeyId}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    # Get all shop cards
    try:
        shopcards = get_shopcards()
        print("Shop cards:", shopcards)
    except Exception as e:
        print("Failed to fetch shop cards:", e)

    # Create a new shop card
    new_shopcard_data = {
        "name": "Sample Shopcard",
        "price": 99.99,
        "description": "This is a sample shop card."
    }
    try:
        created_shopcard = post_shopcard()
        print("Created Shopcard:", created_shopcard)
    except Exception as e:
        print("Failed to create shop card:", e)

    # Delete a shop card by txnKeyId
    txn_key_id_to_delete = "exampleTxnKeyId"
    try:
        delete_response = delete_shopcard(txn_key_id_to_delete)
        print("Deleted Shopcard:", delete_response)
    except Exception as e:
        print("Failed to delete shop card:", e)
