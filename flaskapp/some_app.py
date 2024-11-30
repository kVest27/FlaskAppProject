from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import net as neuronet

app = Flask(__name__)

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'ваш_публичный_ключ'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'ваш_секретный_ключ'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
Bootstrap(app)

class CaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = CaptchaForm()
    if form.validate_on_submit():
        return "reCAPTCHA успешно пройдена!"
    return render_template('form.html', form=form)



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

class NetForm(FlaskForm):
    openid = StringField('OpenID', validators=[DataRequired()])
    upload = FileField('Load Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Send')

@app.route("/net", methods=['GET', 'POST'])
def net():
    form = NetForm()
    filename = None
    neurodic = {}

    if form.validate_on_submit():
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10, './static')
        decode = neuronet.getresult(fimage)

        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]

        form.upload.data.save(filename)

    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)

