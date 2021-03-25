from flask import Flask, render_template, redirect, send_file
from random import randint, choice
import os

from forms import db_session
from forms.forms import RegisterForm
from forms.cans import Can


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
STREET_LIST = ["Автомобилистов", "Баженова", "Васильковая", "Галкина", "Дзержинского",
               "Епифанская", "Жуковского", "Зайцевская", "Индустриальная", "Карла Маркса",
               "Калинина", "Литейзена", "Ложевая", "Мосина", "Невская", "Оборонная", "Павшинский Мост",
               "Революции", "Сойфера", "Токарева", "Фрунзе", "Халтурина", "Циолковского",
               "Чмутова", "Школьная", "Яблочкова"]


@app.route('/')
@app.route('/index')
def index_page():
    return render_template('index.html')


@app.route('/handle', methods=['GET', 'POST'])
def data_input():
    form = RegisterForm()
    if form.validate_on_submit():
        form.street.data = form.street.data if form.street.data != '' else choice(STREET_LIST) + '$' + str(randint(0, 100))
        form.fill.data = form.fill.data if form.fill.data != '' else randint(0, 100)
        form.days.data = form.days.data if form.days.data != '' else randint(0, 1000)

        loc = str(form.street.data)
        fill = str(form.fill.data)
        days = str(form.days.data)

        print('loc:', loc)
        print('fill:', fill)
        print('days:', days)
        return redirect('/add/' + loc + '&' + fill + '&' + days)
    return render_template('data_handle.html', form=form)


@app.route('/add/<data>', methods=['GET', 'POST'])
def random_set(data):
    loc, fill, days = data.split('&')
    db_sess = db_session.create_session()

    can = db_sess.query(Can).filter(Can.loc == loc).first()

    if not can:
        can = Can(
            loc=' '.join(loc.split('$')),
            fill=int(fill),
            days=int(days)
        )
        db_sess.add(can)
    else:
        can.fill = fill
        can.days = days

    db_sess.commit()

    return redirect('/handle')


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    db_sess = db_session.create_session()
    f = open('resive.txt', 'w')
    for i in db_sess.query(Can):
        f.write(str(i.id) + '#' + str(i.loc) + '#' + str(i.fill) + '#' + str(i.days) + '\n')
    f.close()

    return send_file("resive.txt", as_attachment=True)


@app.route('/delete_data/<id>', methods=['GET', 'POST'])
def delete_data(id):
    db_sess = db_session.create_session()
    data = db_sess.query(Can).filter(Can.id == int(id)).first()
    if data:
        db_sess.delete(data)
        db_sess.commit()
    return redirect('/handle')


@app.route('/default/<data>')
def default(data):
    return 'the value is ' + '-'.join(data.split(';'))


if __name__ == "__main__":
    db_session.global_init("data.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
