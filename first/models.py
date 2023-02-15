from first import db , login_manager
from datetime import datetime 
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


    password = db.Column(db.String(60), nullable=False)

    # this is going to hash this . this is et as nullaable set to false .

    posts = db.relationship('Post', backref='author', lazy=True)

     #we havent't added the author to post model . the post model and user model will share one to many relationship as users will author post . this is on to many relationship as one author can hae multiple post but multiple post will have one author.  we set a backref to author . posts attribute has a relationship with post model. The backref is similar to adding another column to post model . What backref does id when we have a post , we can simply use the author attribute to get the user who created this post. the lazy arguement just defines whether it loads the data  as necessary in one go .This is convinient , with this relationship we as with this we can simply use the post created by an individual user.  This is an relationship and not a columnn , we wouldn't see this post coln in database schema , this is running an additional query in the background to get all the posts crated by the user.

    def __repr__(self):

        #this is  called magic methods and dunder methods  how our objects are printed whenever we print it out . __str__ method as well .

        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

    content = db.Column(db.Text, nullable=False)

    #we create in post model as user_id (to specify user in post model ) . we create  user_id / it is a db column . this is the primary key of the user and has relationship with the user model . we specify what it is the foreign key is user_id. since every user is an author . nullable is set to false . if we want to set table name we can set out own table name values /

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):

        return f"Post('{self.title}', '{self.date_posted}','{self.content}')"

