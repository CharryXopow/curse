# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# import base64
# import secrets
# import string
# import pyodbc

# def generate_secret_key(length=32):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     secret_key = ''.join(secrets.choice(characters) for _ in range(length))
#     return secret_key

# app = Flask(__name__)
# app.secret_key = generate_secret_key(28)

# # Функция для подключения к базе данных
# def get_db_connection():
#     conn = sqlite3.connect('base.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/')
# def index():
#     return render_template('login.html')

# # Страница для входа
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         login = request.form['login']
#         password = request.form['password']

#         conn = get_db_connection()
#         user = conn.execute('SELECT * FROM user WHERE login = ? AND password = ?', (login, password)).fetchone()
#         conn.close()

#         if user:
#             session['user_id'] = user['Id']
#             return redirect(url_for('profile'))
#         else:
#             return "Неверный логин или пароль!"

#     return render_template('login.html')

# # Страница для регистрации
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         login = request.form['login']
#         password = request.form['password']

#         conn = get_db_connection()
#         existing_user = conn.execute('SELECT * FROM user WHERE login = ?', (login,)).fetchone()
        
#         if existing_user:
#             conn.close()
#             return "Пользователь с таким логином уже существует!"
        
#         conn.execute('INSERT INTO user (name, login, password,avatar) VALUES (?, ?, ?,1)', (name, login, password))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('login'))

#     return render_template('register.html')

# # Страница профиля
# @app.route('/profile',methods=['GET', 'POST'])
# def profile():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     conn = get_db_connection()

#     if request.method == 'POST':
#         if 'image' in request.files:
#             image_file = request.files['image']
#             image_data = image_file.read()

#             # Добавляем новое изображение в базу данных
#             image_id = conn.execute('select id from image where image_data=?',(image_data,)).fetchone()
#             if image_id is None:
#                 conn.execute('INSERT INTO image (image_data) VALUES (?)', (image_data,))
#                 conn.commit()

#                 image_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
#                 conn.execute('UPDATE user SET avatar = ? WHERE id = ?', (image_id, session['user_id']))
#             else:
#                 conn.execute('UPDATE user SET avatar = ? WHERE id = ?', (image_id[0], session['user_id']))
#             conn.commit()

#     user = conn.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()
#     image = conn.execute('SELECT image.id,image_data FROM user left join image on user.avatar=image.id WHERE user.id = ?', (session['user_id'],)).fetchone()
#     conn.close()

#     # Декодируем изображение для отображения
#     image_data = base64.b64encode(image['image_data']).decode('utf-8') if image else None

#     return render_template('profile.html', name=user['name'], image_data=image_data)

# # Выход из профиля
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run()
