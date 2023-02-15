from flask import render_template, url_for, flash, redirect,request,abort
from first import app,db,bcrypt
import secrets
import os 
from PIL import Image
from first.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm
from first.models import User, Post
from flask_login import login_user, current_user,logout_user, login_required
#importing request from flask to request the account redirect after login is comepleted





# posts = [
#     {
#         'author': 'Harsh Upreti',    
#         'title': 'Programming made easy',
#         'content': 'This Book teaches you programming using Flask ',
#         'date_posted': 'April 20, 2022'
#     },
#     {
#         'author': 'Ashwin Kumar',
#         'title': 'Gaming made easy',
#         'content': 'This Book teaches you how to become a gamer',
#         'date_posted': 'September 21, 2022'
# }
# we no longer pass dummy data here now . Instead we can use our newly created data .
# ]
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
# this is the register route that takes methods as get and from post
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data , email = form.email.data ,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()  
        #get the first occurence of any similar email that exists in the form already > IF so we have a problem , we don;t need to allow registration of this similar username :) 
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            #we check if the password the user puts in is same as compared to the one we get from the login password field. so if the user (particular one here) hashed password is qual to the password we get from the login password field . the password matches and we allow login of the user else we don;t allow and give the warning either username same or password incorrect 
            
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # We create a new function called login_user which has function and can take user and also remember me arguement . checked it will br true else false . 
            return redirect( url_for('home'))
            
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
@app.route("/logout")
def logout(): # we create a logout route here and we call this route logout route . We use the logout)user function to log out users 
    logout_user()
    #this basically calls the logout function and we simply call the functions with no parameters since it knows what user were logged in and now we also need to see a logout in our navigation template , so we need to change our navigation template as well . 
    return redirect( url_for('home'))
#we create a route for the user's account that they can access once they are logged in . 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #we need the file extension that the file originally had . to know about it , we need to import os module.
    _,f_ext=os.path.splitext(form_picture.filename)
    #if u want to throw away a variable name is to use an underscore . so it will store it no where .
    #here we only need the file extension.
    picture_fn = random_hex +f_ext
    #app.root_path will give us file path all the way to our package directory 
    picture_path= os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = ( 125 , 125 ) 
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/post/new",methods=["POST","GET"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content = form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form ,legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    post  = Post.query.get_or_404(post_id)
    return render_template('post.html',title = post.title , post = post)

@app.route("/post/<int:post_id>/update")
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!= current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        #we don;t add because this is something already in the database . we are not adding anything here :
        db.session.commit()
        flash('Your post has been updated !' ,'success')
        return redirect(url_for('post',post_id=post.id))  
    elif request.method=='GET':
        form.title.data= post.title 
        form.content.data = post.content
   # we populate our s form with the values
    return render_template('create_post.html',title = "Update Post ",form=form,legend = "Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/account",methods=['GET', 'POST'])
@login_required
# so now our extension knows we need to login in but we need to tell our extension where our login route is located . we got to init.py and right where we created the login manager we need to write login_manager.login_view and set it equal to login ( function name for our route ) same as what we write for our url_for method.
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data)
            current_user.image_file = picture_file
        #now if we look into it the image is very large
        current_user.username = form.username.data
        current_user.email =  form.email.data
        db.session.commit()
        flash('your account has been updated !','success')
        return redirect(url_for('account'))
        #we will need to put a return redirect because of something called post get redirect pattern , basically if we press submit it will submit the data via post to the database and below line is an redirect line , so it will redirect using get and before redirecting will post the data out of the form to the server . So in this case ,it send the data twice and to avoid this we redirect to a  new page with any random customised message. 
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # this above is to populate the fields with existing data , will hit only when 
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)
    #we pass the image_file since we know that we can do this while renderering templates we can pass parameters to it 
#now we create the account template within our template directory .


    #now in routes i need to look for a way by which i can restrict access to certain routes for example if user clicks on a link to twitter profile or something like that then it should check if the user is logged in , if not then it should prompt / redirect the user to the login page.Now if i get the url for account page and i type it and hit enter , it should have a check in page , the user should login to access this page . We download thw login required decorator now for it .we need to add the login_required decorator to out account route .
    # coming to the next_page . we can get it from request.args and getting the value in next . Now args is a dictionary so we could have used a dictionary ['next'] but if they key doesn;t exist at some point , it will throw an error . hence if the next paramater exists it will be equal to the route else it will give None 



#we need to add in our account.html ( in the username and email fields ) we need them to automatically have our current user name and current email filled in . SO it would be better in that case that we have 



#sql alchemy also allows users to change and update the user vrriables very quickly  so that is a plus point of sql alchemy.