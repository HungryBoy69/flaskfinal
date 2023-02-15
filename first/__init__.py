from operator import methodcaller
from flask import *
from flask_bcrypt import Bcrypt
from xmlrpc.client import DateTime
from datetime import *
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_login import LoginManager
env = Environment(
    loader=PackageLoader("first"),
    autoescape=select_autoescape()  
                 )


app = Flask(__name__)

app.config['SECRET_KEY']='f059fdf5b1ddd0fdfa77128cb2079c93b7a6eef4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='danger'
from  first import routes
#here we set the login_manager.login_view to login so every time we access a page we were not supposed to . we will get redirected to the login page with the default msg . but we were using bootstrap classes till now , so we use the login_manager.login_message_category instead and pass the info in the category parameter which in turn will add the blue bootstrap color to it .

# another problem we face here is that once  get thrown to login page to login . After the login gets done , we should redirect it back to the page the user was trying to access. On investigating i found that there was a query parameter int he url that said login?next=%2Faccount .So if we can access that that def we can change the route back to it (redirect the user there). HEnce we need to import a request object to do so . Let us go to routes and import request object from flask and change the next query after the user has logged in