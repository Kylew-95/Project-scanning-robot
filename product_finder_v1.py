from camera import scan_code
import openfoodfacts

api = openfoodfacts.API(user_agent="openfoodfacts-scanner")

barcode_data = scan_code()


def get_product_info(barcode_data):
    for data in barcode_data:
        product_info = api.product.get(data)
        print(product_info)


get_product_info(barcode_data)
