from flask_login import current_user
from app import app
from flask import request
from .apiauthhelper import token_required
from werkzeug.security import check_password_hash
from app.models import SavedArticles, SavedCategories, User
from app.models import db


from .models import User

import requests


@app.route('/api/addcategory', methods=["POST"])
@token_required
def addCategoryAPI(user):
    data = request.json
    category = data['category']
    all_cats = SavedCategories.query.filter_by(user_id=user.id).all()
    all_cats=[p.category for p in all_cats]
    print(all_cats,"hi")
    if category not in all_cats:
        new_category = SavedCategories(category, user.id)
        new_category.save()
        return {
            'status': 'ok',
            'message': f"{category} succesfully saved"
        }
    else:
        return {
            'status': 'ok',
            'message': f"{category} already saved"
        }



@app.route('/api/savedcategories/<int:user_id>')
def SavedCategoriesAPI(user_id):
    categories = SavedCategories.query.filter_by(user_id=user_id).all()
    my_cats= [p.category for p in categories]
    search_string=''
    if len(my_cats)>1:
        for each in my_cats:
            search_string+=f'{each}+AND+'
        search_string=search_string[:-5]
    else:
        search_string=my_cats[0]
    print(search_string)
    print(my_cats)
    return {'status': 'ok', 'total_results': len(categories), "categories": my_cats, 'search':search_string}


@app.route('/api/delcategory', methods=["POST"])
@token_required
def delCategoryAPI(user):
    data = request.json 
    category = data['category']
    del_category = SavedCategories.query.filter_by(category=category,user_id=user.id).first()
    print(del_category)
    del_category.delete()
    return {
        'status': 'ok',
        'message': f"{category} succesfully deleted"
    }


@app.route('/api/savedarticles', methods=['POST'])
@token_required
def SaveArticlesAPI(user):
    data = request.json 
    title=data['title']
    author=data['author']
    source_name=data['source_name']
    description=data['description']
    url=data['url']
    url_image=data['url_image']
    published_at=data['published_at']
    print(title)
    new_article = SavedArticles(title,author,source_name,description, url, url_image, published_at,user.id)
    new_article.save()

    return {
        'status': 'ok',
        'message': f"Article {title} succesfully saved"
    }
@app.route('/api/savedarticles/<int:user_id>')
def GetSavedArticlesAPI(user_id):
    articles = SavedArticles.query.filter_by(user_id=user_id).all()
    my_arts= [p.to_dict() for p in articles]
    print(articles)
    return {'status': 'ok', 'total_results': len(articles), 'articles':my_arts}

@app.route('/api/delarticle', methods=["POST"])
@token_required
def delArticleAPI(user):
    data = request.json 
    article = data['article']
    del_article = SavedArticles.query.filter_by(title=article,user_id=user.id).first()
    print(del_article)
    del_article.delete()
    return {
        'status': 'ok',
        'message': f"{article} succesfully deleted"
    }
