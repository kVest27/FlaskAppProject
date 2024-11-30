#!/bin/bash
export FLASK_APP=some_app.py
flask run --host=0.0.0.0 --port=5000
gunicorn --bind 127.0.0.1:5000 wsgi:app & APP_PID=$!
sleep 5
echo "Start client tests"
python3 client.py
sleep 5
echo $APP_PID
kill -TERM $APP_PID
echo "Gunicorn process terminated"
exit $?

echo "Запуск клиента для тестирования API..."
python3 client.py
APP_CODE=$?

echo "Остановка сервера..."
kill -TERM $APP_PID

exit $APP_CODE
