from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed 
#we use this to type of field and file allowed as validator ( what kind of files we wat to be uploaded)
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from first.models import User 
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError

# we create  a  registration field class that will be having variables of type mentioned . We can also see this as classes with variables having some validation rules . inside this we can also create functions that has some custom validation functionalities inside it .
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        if current_user.is_authenticated:
            if username.data != current_user.username:
                user  = User.query.filter_by(username = username.data).first()
            #here we pass the filter to all the users by saying filter out the first found username where username = username.data ( this is from the form we get in forms.py . then  we pass the user to the if condition , and if user is not none( that means we have found the first occurence of such username) it will print the validation error message ! 
                if user :
                    raise ValidationError('Username is already taken ! Please choose a different username')  
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is already taken ! Please choose a different email')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# what we do here is we create a class that will be named update account form and will check whether the user name and email that we recieve from the current_user is different from the new one we wanna change that;s when the updation should work . so we import current_user and then check it under an if statement to see if they are similar or not .


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    # we are setting the field of the form for image
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user  = User.query.filter_by(username = username.data).first()
                #here we pass the filter to all the users by saying filter out the first found username where username = username.data ( this is from the form we get in forms.py . then  we pass the user to the if condition , and if user is not none( that means we have found the first occurence of such username) it will print the validation error message ! 
            if user :
                raise ValidationError('Username is already taken ! Please choose a different username')  
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email is already taken ! Please choose a different email')
#BREAKING: The is_authenticated, is_active, and is_anonymous members of the user class are now properties, not methods. Applications should update their user classes accordingly.


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
                