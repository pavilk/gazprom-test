import json

inData = '{"one": ["http", "yandex.ru"], "two": ["https", "google.com"]}'
outData = json.loads(inData)

if __name__ == "__main__":
    print(type(outData))
