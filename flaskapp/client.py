import requests
import os
import base64

# Тестируем главный маршрут
r = requests.get('http://localhost:5000/')
print(r.status_code)
print(r.text)

# Тестируем маршрут /data_to
r = requests.get('http://localhost:5000/data_to')
print(r.status_code)
print(r.text)

path = os.path.join('./static', 'image0008.png')

with open(path, 'rb') as fh:
    img_data = fh.read()
    b64 = base64.b64encode(img_data)

jsondata = {'imagebin': b64.decode('utf-8')}
res = requests.post('http://localhost:5000/apinet', json=jsondata)

if res.ok:
    print(res.json())
else:
    print(f"Ошибка: {res.status_code}, {res.text}")

try:
    r = requests.get('http://localhost:5000/apixml')
    print(r.status_code)
    if r.status_code != 200:
        print("Ошибка сервера")
        exit(1)
    print(r.text)
except Exception as e:
    print(f"Ошибка клиента: {e}")
    exit(1)
