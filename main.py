from flask import Flask, request, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#database model for blog posts


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(120))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, foreign_key = True(User))

    def __init__(self, title, subtitle, date, content):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date = date
        self.content = content

class User(db.Model): #database model for users

    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


#routes

# @app.route('/') #route or home page displaying all posts
# def index():
#     current_posts = Blog.query.order_by(Blog.id.desc()).all()
#     return render_template('index.html', current_posts=current_posts)


# @app.route('/register', methods=['GET', 'POST'])  # route to registration page
# def register():
#     if request.method == 'POST':
#         # if user submits input check db for email.
#         #grab email from form & check db for presence of email
#         email = User.query.filter_by(request.form('email')).first()
#         #then process registration and add to db
#         if email not in email:
#             email = request.form('email')
#             username = request.form('username')
#             password = request.form('password')
#             verify_password = request.form('verify_password')
#             #verify passwords
#             if verify password in password:  # add info to db and send user to the main page
#                 user = User(username, email, password)
#                 db.session(user)
#                 db.commit()
#                #create a session for the current user
#                 return redirect(url_for('/'))
#             #TODO if passwords dont match flash error and return register page with ps fields empty
#         # TODO alert user that and account already exists and send to log in
#         return redirect(url_for('login'))
#     return render_template('register.html')


# @app.route('login', methods= ['GET', 'POST'])  # route or home page displaying all posts
# def login():
#     if request.method == 'POST':
#         #if the user logs in check db for presence of email
#         email = User.query.filter_by(request.form('email')).first()
#         password = User.query.filter_by(request.form('password')).first()
#         if password in User.password:
#             redirect(url_for('/'))
#     return render_template('login.html')



# @app.route('/post/<int:new_post_id>') 
# #route to show individual post filtered by that particuar post's id
# def post(new_post_id):
#     new_post = Blog.query.filter_by(id=new_post_id).first_or_404()
#     return render_template('post.html', new_post=new_post)

# #processes post form and adds entry to database

# @app.route('/add_post', methods=['GET', 'POST'])
# def add_post():
#     if request.method == 'POST':
#         new_title = request.form['title']
#         if not new_title:
#             error = "Please enter a title."
#             return render_template('add_post.html', error=error)

#         new_subtitle = request.form['subtitle']
#         new_author = request.form['author']
#         new_content = request.form['content']
#         date = datetime.now()
#         new_post = Blog(new_title, new_subtitle, new_author, date, new_content)
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for(''))

#     return render_template('add_post.html')


if __name__ == '__main__':
    app.run()
