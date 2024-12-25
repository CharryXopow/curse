from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user, current_user
from models import db,SalesFeed,User,Painting,Comment
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'abcddfg'

AVATAR_UPLOAD_FOLDER = os.path.join(app.root_path,'static/avatars/')
app.config['UPLOAD_FOLDER'] = AVATAR_UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(AVATAR_UPLOAD_FOLDER):
    os.makedirs(AVATAR_UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({"success": False, "message": "No file part"})

    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.user_id}_{filename}")
        
        file.save(avatar_path)
        
        # Обновляем путь в базе данных
        current_user.avatar_url = f"avatars/{os.path.basename(avatar_path)}"
        db.session.commit()

        return jsonify({"success": True, "avatar_url": url_for('static', filename=current_user.avatar_url)})
    else:
        return jsonify({"success": False, "message": "Invalid file type"})

@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).fetchone()
            return f"Database connection successful: {result[0]}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"
    
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class CurrentUser(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String, nullable=True)
    card_number = db.Column(db.String(16), nullable=True)
    card_expiry_date = db.Column(db.String(5), nullable=True)
    card_cvv = db.Column(db.String(3), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(CurrentUser,user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = CurrentUser.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash,password):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Неправильный логин или пароль')  
    return render_template('login.html')


@app.route('/')
def index():
    with app.app_context():
        sales_feed = db.session.query(SalesFeed).options(
            joinedload(SalesFeed.user),
            joinedload(SalesFeed.painting)
        ).all()

        # Вывод для отладки
        for post in sales_feed:
            print(f"Post ID: {post.post_id}, User: {post.user.username}, Painting: {post.painting.title}")

    return render_template('sales_feed.html', sales_feed=sales_feed)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)
    
    user = CurrentUser(user_id='1',username=username, email=email, password_hash=hashed_password)

    db.session.add(user)
    db.session.commit()
    flash('Вы успешно зарегистрировались.')
    user = CurrentUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect(url_for('profile'))
    # return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
