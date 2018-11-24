import json


def get_product_data():
    data = dict()

    data["phone"] = json.dumps({"test": 1})

    return data