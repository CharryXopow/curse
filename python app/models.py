from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
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
    created_at = db.Column(db.DateTime, nullable=False)

class Painting(db.Model):
    __tablename__ = 'paintings'
    painting_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(20), db.ForeignKey('users.user_id'),nullable=False)
    title = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    image_url = db.Column(db.String, nullable=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.String(max), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)

    artist = db.relationship('User', foreign_keys=[artist_id],backref='paintings_artist')
    owner = db.relationship('User', foreign_keys=[owner_id], backref='paintings_owner')

class SalesFeed(db.Model):
    __tablename__ = 'sales_feed'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    painting_id = db.Column(db.Integer, db.ForeignKey('paintings.painting_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', foreign_keys=[user_id],backref='sales_feed')
    painting = db.relationship('Painting', foreign_keys=[painting_id], backref='sales_feed_posts')

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('sales_feed.post_id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    comment_text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='comments')
    post = db.relationship('SalesFeed', foreign_keys=[post_id], backref='comments_post')

class UserLikes(db.Model):
    __tablename__ = 'user_likes'
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('sales_feed.post_id'), nullable=False)
    like_date = db.Column(db.DateTime, nullable=False)
    canceled = db.Column(db.Boolean,nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='user_likes')
    like = db.relationship('SalesFeed', foreign_keys=[post_id], backref='user_likes_posts')

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    isActual = db.Column(db.Boolean,nullable=False)

class PaintingTags(db.Model):
    __tablename__ = 'painting_tags'
    painting_id = db.Column(db.Integer, db.ForeignKey('paintings.painting_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    deleted = db.Column(db.Boolean,nullable=False)

    painting = db.relationship('Painting', foreign_keys=[painting_id], backref='painting_tags')
    tag = db.relationship('Tags', foreign_keys=[tag_id], backref='painting_tags_Tags')

class Contracts(db.Model):
        __tablename__ = 'contracts'
        id = db.Column(db.String(20),primary_key=True)
        cdate = db.Column(db.DateTime, nullable=False)
        client_id = db.Column(db.String(20), db.ForeignKey('users.user_id'))
        post_id = db.Column(db.Integer, db.ForeignKey('sales_feed.post_id'), nullable=False)
        price = db.Column(db.Numeric(10,2), nullable=False)

        client = db.relationship('User', foreign_keys=[client_id],backref='contracts')
        post = db.relationship('SalesFeed', foreign_keys=[post_id], backref='contracts_post')
