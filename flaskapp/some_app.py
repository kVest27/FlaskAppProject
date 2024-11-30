from flask import Flask
from flask import render_template

app = Flask(__name__)

# Декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return "<html><head></head><body>Hello World!</body></html>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

@app.route("/data_to")
def data_to():
    # Создаем данные для передачи в шаблон
    some_pars = {'user': 'Ivan', 'color': 'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    
    # Передаем данные в шаблон
    return render_template('simple.html', 
                           some_str=some_str, 
                           some_value=some_value, 
                           some_pars=some_pars)
