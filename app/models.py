from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }

    def saveToDB(self):
        db.session.commit()

    

class SavedCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, category,user_id):
        self.category=category
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdates(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'user_id': self.user_id
        }


class SavedArticles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(500), nullable=False)
    source_name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(750), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    url_image = db.Column(db.String(500))
    published_at = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self,title,author,source_name, description, url, url_image, published_at,user_id):
        self.title=title
        self.author=author
        self.source_name=source_name
        self.description=description
        self.url=url
        self.url_image=url_image
        self.published_at=published_at
        self.user_id = user_id

   
    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdates(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'title':self.title,
            'author':self.author,
            'source_name': self.source_name, 
            'description': self.description,
            'url': self.url,
            'url_image':self.url_image,
            'published_at':self.published_at,
            'user_id': self.user_id
        }
