from flask import Blueprint,request

from ..apiauthhelper import token_required
#import login funcitonality
from flask_login import current_user
from werkzeug.security import check_password_hash

# import models
from app.models import SavedArticles, SavedCategories, User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db



# @auth.route('/login', methods = ["GET","POST"])
# def logMeIn():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))

#     form = LoginForm()
#     if request.method == "POST":
#         if form.validate():
#             username = form.username.data
#             password = form.password.data
#             # Query user based off of username
#             user = User.query.filter_by(username=username).first()
#             print(user.username, user.password, user.id)
#             if user:
#                 # compare passwords
#                 if check_password_hash(user.password, password):
#                     flash('You have successfully logged in!', 'success')
#                     login_user(user)
#                     return redirect(url_for('index'))
#                 else:
#                     flash('Incorrect username/password combination.', 'danger')
#             else:
#                 flash('User with that username does not exist.', 'danger')

#     return render_template('login.html', form=form)

# @auth.route('/logout')
# @login_required
# def logMeOut():
#     flash("Successfully logged out.", 'success')
#     logout_user()
#     return redirect(url_for('auth.logMeIn'))

# @auth.route('/signup', methods=["GET", "POST"])
# def signMeUp():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = UserCreationForm()
#     if request.method == "POST":
#         print('POST request made')
#         if form.validate():
#             username = form.username.data
#             email = form.email.data
#             password = form.password.data

#             # add user to database
#             user = User(username, email, password)

#             # add instance to our db
#             db.session.add(user)
#             db.session.commit()
#             flash("Successfully registered a new user", 'success')
#             return redirect(url_for('auth.logMeIn'))
#         else:
#             flash('Invalid form. Please fill it out correctly.', 'danger')
#     return render_template('signup.html', form = form)


##### API ROUTES #########
@auth.route('/api/signup', methods=["POST"])
def apiSignMeUp():
    data = request.json
     
    username = data['username']
    email = data['email']
    password = data['password']

    # add user to database
    user = User(username, email, password)

    # add instance to our db
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully created user {username}"
    }


from app.apiauthhelper import basic_auth, token_auth

@auth.route('/token', methods=['POST'])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }


@auth.route('/api/login', methods=["POST"])
def apiLogMeIn():
    data = request.json

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user:
        # check password
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }
        return {
            'status': 'not ok',
            'message': "Incorrect password."
        }
    return {
        'status': 'not ok',
        'message': 'Invalid username.'
    }


@auth.route('/api/addcategory', methods=["POST"])
@token_required
def addCategoryAPI(user):
    data = request.json # this is coming from POST request Body

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



@auth.route('/api/savedcategories/<int:user_id>')
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
# else:
#     return {
#         'status': 'not ok',
#         'code': 'Invalid Pin',
#         'message': 'The pin number was incorrect, please try again.'
#     }


@auth.route('/api/delcategory', methods=["POST"])
@token_required
def delCategoryAPI(user):
    data = request.json # this is coming from POST request Body

    category = data['category']
    

    del_category = SavedCategories.query.filter_by(category=category,user_id=user.id).first()
    print(del_category)
    del_category.delete()
    return {
        'status': 'ok',
        'message': f"{category} succesfully deleted"
    }


@auth.route('/api/savedarticles', methods=['POST'])
@token_required
def SaveArticlesAPI(user):
    data = request.json # this is coming from POST request Body
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
@auth.route('/api/savedarticles/<int:user_id>')
def GetSavedArticlesAPI(user_id):
    articles = SavedArticles.query.filter_by(user_id=user_id).all()
    my_arts= [p.to_dict() for p in articles]
    print(articles)
   
    return {'status': 'ok', 'total_results': len(articles), 'articles':my_arts}
# else:
#     return {
#         'status': 'not ok',
#         'code': 'Invalid Pin',
#         'message': 'The pin number was incorrect, please try again.'
#     }
@auth.route('/api/delarticle', methods=["POST"])
@token_required
def delArticleAPI(user):
    data = request.json # this is coming from POST request Body

    article = data['article']
    

    del_article = SavedArticles.query.filter_by(title=article,user_id=user.id).first()
    print(del_article)
    del_article.delete()
    return {
        'status': 'ok',
        'message': f"{article} succesfully deleted"
    }
