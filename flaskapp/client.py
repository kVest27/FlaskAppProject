import requests

# Тестируем главный маршрут
r = requests.get('http://localhost:5000/')
print(r.status_code)
print(r.text)

# Тестируем маршрут /data_to
r = requests.get('http://localhost:5000/data_to')
print(r.status_code)
print(r.text)
