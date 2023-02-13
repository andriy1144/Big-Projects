from flask import Flask, render_template, request, session

from DB import UseDatabase

app = Flask(__name__)

#app.config['config'] = {... -> Info to connect database}

app.secret_key = 'YouWillNeverKnowMyCodHaHaHAHAah'


def note_request(user, passw, name, note) -> object:
    with UseDatabase(app.config['config']) as cursor:
        _SQL = '''insert into notebb2
      (user,passwword,title,pharas)
      values
      (%s,%s,%s,%s)'''
        cursor.execute(_SQL, (user, passw, name, note))

def user_log(login,password):
    with UseDatabase(app.config['config']) as cursor:
        _SQL = '''insert into use_pasw
        (user,password)
        values
        (%s,%s)'''
        cursor.execute(_SQL,(login,password))


@app.route('/thx', methods=['POST'])
def thx_page():
    login = request.form['login']
    passw = request.form['passwd']
    passw2 = request.form['passwd2']
    with UseDatabase(app.config['config']) as cursor:
        _SQL = '''select user from use_pasw'''
        cursor.execute(_SQL)
        users = cursor.fetchall()
        for user in users:
            user_list = user
    if bool(login) == True and bool(passw) == True and bool(passw2) == True and len(passw) >= 8 and passw == passw2:
        if bool(users):
            if login not in user_list:
                session['user'] = login
                session['passw'] = passw
                user_log(login, passw)
                return render_template('index3.html', the_title='Успішно', the_warn='Регистрація пройшла успішно')
            else:
                return render_template('index4_reg.html', the_title='Регистрація',
                                       the_w='Цей логін зайнятий ,попробуйте інший')
        else:
            session['user'] = login
            session['passw'] = passw
            user_log(login, passw)
            return render_template('index3.html', the_title='Успішно', the_warn='Регистрація пройшла успішно')
    else:
        return render_template('index4_reg.html', the_title='Регистрація', the_w='Будь ласка введіть свій новий логін '
                                                                                 'і пароль. (Пароль має бути більший '
                                                                                 '8-ми символів)')


@app.route('/')
def page():
    if 'user' in session and 'passw' in session:
        with UseDatabase(app.config['config']) as cursor:
            _SQL = f'''select title,pharas from notebb2 where user = '{session['user']}' '''
            cursor.execute(_SQL)
            data = cursor.fetchall()
        return render_template('index1.html', the_title='Нотатки', the_user=session['user'], the_link='/logout',
                               the_log_text='Вийти', the_datas=data, the_style='reg_text_log')
    else:
        return render_template('index1.html', the_title='Нотатки', the_link='/reg',
                               the_log_text='Реєстрація', the_style='reg_text')


@app.route('/reg')
def reg_page():
    return render_template('index4_reg.html', the_title='Регистрація')


@app.route('/index2.html')
@app.route('/')
def page_void():
    if 'user' in session and 'passw' in session:
        return render_template('index2.html', the_title='Нотатки', the_user=session['user'], the_link='/logout',
                               the_log_text='Вийти', the_style='reg_text_log')
    else:
        return render_template('index1.html', the_title='Нотатки', the_warn4='Будь ласка виканайте регистрацію aбо авторизацію',
                               the_link='/reg',
                               the_log_text='Регистрація', the_style='reg_text')


@app.route('/login')
def login_page():
    return render_template('index5_log.html',the_title = 'Нотатки')


def log_check(log):
    with UseDatabase(app.config['config']) as cursor:
        _SQL = '''select user from use_pasw'''
        cursor.execute(_SQL)
        user_list = cursor.fetchall()
    b = 0
    while b < len(user_list):
        if log in user_list[b]:
            return user_list[b]
            b = 0
            break
        else:
            b += 1

@app.route('/thx_for_log', methods=['POST'])
def page_thx_log():
    login = request.form['check_login']
    password = request.form['check_passwd']
    log_MAIN = log_check(login)
    if bool(log_MAIN) == True:
        with UseDatabase(app.config['config']) as cursor:
            _SQL = f'''select * from use_pasw where user = %s '''
            cursor.execute(_SQL,log_MAIN)
            main_user = cursor.fetchall()
        if bool(login) == True and bool(password) == True:
            if login == main_user[0][0] and password == main_user[0][1]:
                session['user'] = login
                session['passw'] = password
                return render_template('index3.html', the_title='Нотатки',
                                           the_warn='Авторизація пройшла успішно')
            else:
                 return render_template('index5_log.html', the_title='Нотатки',
                                           the_w='Логін або пароль було введено неправильно')
        else:
            return render_template('index5_log.html', the_title='Нотатки', the_w='Введіть свій логін і пароль')
    else:
        return render_template('index5_log.html', the_title='Нотатки', the_w='Такого користувача не існує. Виконайте регистрацію')


@app.route('/logout')
def page_logout():
    session.pop('user')
    session.pop('passw')
    return render_template('index3.html', the_title='Нотатки',
                           the_warn='Ви вийшли з акаунту')


@app.route('/index3.html', methods=['POST'])
def page_th():
    title = request.form['title']
    note = request.form['note']
    if bool(title) == True and bool(note) == True:
        note_request(session['user'], session['passw'], title, note)
        return render_template('index3.html', the_title='Нотатки', the_warn='Ваш відгук збережено')
    else:
        return render_template('index3.html', the_title='Нотатки',
                               the_warn='Щоб щось зберегти, потрібно спершу написати')


app.run(debug=True)
