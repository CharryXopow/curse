from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Создаем один экземпляр SQLAlchemy

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar_url = db.Column(db.String(200), nullable=True)  # URL аватара
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    # card_info = db.Column(db.String(100), nullable=True)

class Painting(db.Model):
    __tablename__ = 'paintings'
    painting_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)  # URL изображения
    price = db.Column(db.Float, nullable=False)

    owner = db.relationship('User', backref='paintings')

class SalesFeed(db.Model):
    __tablename__ = 'sales_feed'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    painting_id = db.Column(db.Integer, db.ForeignKey('paintings.painting_id'), nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    repost_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='sales_feed')
    painting = db.relationship('Painting', backref='sales_feed_posts')

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('sales_feed.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('SalesFeed', backref='comments')
    user = db.relationship('User', backref='user_comments')
