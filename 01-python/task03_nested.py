def get_item(data: dict, keys: str):
    for key in keys.split("."):
        data = data[key]
    return data
