from Scanner import scan_code, stored_barcodes
import requests
import json
import os

# script_dir = os.path.dirname(os.path.abspath(__file__))

# json_file = os.path.join(script_dir, '..', 'dummy.json')
# with open(json_file, 'r') as file:
#     dummy_json_data = file.read()

# product_data = json.loads(dummy_json_data)

# WORKed**** need to touch no clue why it doesnt return my data now


def fetch_product_data():
    global product_data
    for get_barcode_data in stored_barcodes:
        print("get barcode", get_barcode_data)
        params = {
            'api_key': '6D090B19E8B64904A5D2601CBE7A5FDA',
            'amazon_domain': 'amazon.co.uk',
            'gtin': get_barcode_data,
            'type': 'product'
        }

        # make the http GET request to Rainforest API
        api_result = requests.get(
            'https://api.rainforestapi.com/request', params)

        # parse the JSON response
        product_data = json.dumps(api_result.json())

    return product_data

# print(f"my stored: {stored_barcodes}")


def get_product_info():
    for barcodes in stored_barcodes:
        if barcodes in product_data['request_parameters']['gtin']:
            title = product_data['product']['title']
            # img = product_data['product']['main_image']['link']
            print(title)
            return (title)
