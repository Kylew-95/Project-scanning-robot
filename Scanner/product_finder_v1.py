from Scanner.camera import scan_code
import requests
import json
with open('dummy.json', 'r') as file:
    dummy_json_data = file.read()

product_data = json.loads(dummy_json_data)


barcode_data = scan_code()


# WORKS DONT TOUCH
# for get_barcode_data in barcode_data:

#     print("get barcode", get_barcode_data)
#     params = {
#         'api_key': '6D090B19E8B64904A5D2601CBE7A5FDA',
#         'amazon_domain': 'amazon.co.uk',
#         'gtin': get_barcode_data,
#         'type': 'product'
#     }

#     # make the http GET request to Rainforest API
#     api_result = requests.get('https://api.rainforestapi.com/request', params)

#     # parse the JSON response
#     api_result_json = json.dumps(api_result.json())

#     print(api_result_json)


for barcodes in barcode_data:
    if barcodes in product_data['request_parameters']['gtin']:
        print(product_data['product']['title'])
