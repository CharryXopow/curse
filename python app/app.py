from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user, current_user
from models import db,SalesFeed,User,Painting,Comment
from sqlalchemy import text
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'

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
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255))

    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return CurrentUser.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = CurrentUser.query.filter_by(email=email).first()
        if user and user.password_hash == password:
            login_user(user)
            return redirect(url_for('index'))
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
    user = CurrentUser(username=username, email=email, password_hash=password)
    db.session.add(user)
    db.session.commit()
    flash('Вы успешно зарегистрировались, теперь войдите в аккаунт.')
    return redirect(url_for('login'))

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
