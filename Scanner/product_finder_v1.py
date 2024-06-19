from Scanner import stored_barcodes
# from camera import scan_code, stored_barcodes
import requests
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

json_file = os.path.join(script_dir, '..', 'dummy.json')
with open(json_file, 'r', encoding='utf-8') as file:
    dummy_json_data = file.read()

product_data_list = []
product_data_list.append(json.loads(dummy_json_data))

# WORKed**** need to touch no clue why it doesnt return my data now


# def fetch_product_data():
#     all_product_data = []

#     for get_barcode_data in stored_barcodes:
#         params = {
#             'api_key': '6D090B19E8B64904A5D2601CBE7A5FDA',
#             'amazon_domain': 'amazon.co.uk',
#             'gtin': get_barcode_data,
#             'type': 'product',
#             'encoding': 'utf-8',
#         }

#         # Make the HTTP GET request to Rainforest API
#         api_result = requests.get(
#             'https://api.rainforestapi.com/request', params=params)

#         # Parse the JSON response
#         product_data = api_result.json()
#         # Add the product data to the list
#         all_product_data.append(product_data)
#         print(product_data)

#     return all_product_data


def get_product_info():
    # product_data_list = fetch_product_data()
    for product_data in product_data_list:
        for barcode in stored_barcodes:
            if product_data['request_parameters']['gtin'] in barcode:
                title = product_data['product']['title']
                # Assuming also_bought is a list, accessing the first item
                symbol = '£'
                price = product_data['also_bought'][1]['price']['value']

    return (title, symbol, price)
