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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, subtitle, date, content, owner):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.content = content
        self.owner = owner

class User(db.Model): #database model for users

    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    owner_post = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


def validate(form_input):
    #check for presence of input
    form_value = form_input
    error = ''
    if not form_input:
        error = "Why you no enter {name} !?"

    elif len(form_value) < 3 or len(form_value) > 20:  # check for length
        error = "I need something between (3-20) characters"

    elif " " in form_value:  # check for spaces
        error = "Me no likey {name} with spaces"
    return error

#routes

@app.route('/') #route or home page displaying all posts
def index():
    current_posts = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('index.html', current_posts=current_posts)


@app.route('/register', methods=['GET', 'POST'])  # route to registration page
def register():
    if request.method == 'POST':
        #if user submits form pull input from form 
        email = request.form['email']
        username = request.form['username' ]
        password = request.form['password' ]
        verify_password = request.form['verify_password']
        #TODO validate input
        user_name_error = ""
        password_error = ""
        verify_pass_error = ""
        email_error = ""
        # #checks for validation of username, password, and verify password
        user_name_error = validate(username).format(name="Username")
        password_error = validate(password).format(name="Password")
        verify_pass_error = validate(verify_password).format(name="Verify Password")
        email_error = validate(email).format(name="Email") 
        
        # #compare password to verify password
        if verify_password not in password:
            #TODO flash error compare_pass_error = "NONE SHALL PASS!...Without matching passwords"
            
        #check email for @ and . symbols
        if not re.search(r"([a-z]+[@]+[a-z]+[.]+[a-z])", email):
            #TODO flash email_error = "Can I get an actual email address?" 
    
        #checks for empty error messages if there are no errors validation passes can move on to checking db for user
        if not (user_name_error or
                password_error or
                verify_pass_error or
                compare_pass_error or
                email_error
                ):
        #Check if user exists in db
            existing_user= User.query.filter_by(email=email).first()
            if not existing_user: #make a new user if not existing
                new_user= User(username, email, password)
                db.session.add(new_user)
                db.commit()
                #TODO create session to remember user & flash to welcome user to index
                return redirect('/')
            else:
                #TODO tell user they already exist in db
                pass
        return render_template('register.html',
                               username_error=user_name_error,
                               password_error=password_error,
                               verify_pass_error=verify_pass_error,
                               compare_pass_error=compare_pass_error,
                               email_error=email_error,
                               user_name=user_name,
                               )
           
    return render_template('register.html') #TODO make flashes for all error messages


@app.route('login', methods= ['GET', 'POST'])  # route or home page displaying all posts
def login():
    if request.method == 'POST':
        #if the user logs in check db for presence of email
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return redirect('/')
        else:
            #TODO explain why log in failed
            pass
    return render_template('login.html')



# @app.route('/post/<int:new_post_id>') 
# #route to show individual post filtered by that particuar post's id
# def current_post(new_post_id):
#     new_post = Blog.query.filter_by(id=new_post_id).first_or_404()
#     return render_template('post.html', new_post=new_post)

# #processes post form and adds entry to database

# @app.route('/add_post', methods=['GET', 'POST'])
# def add_post():
#     if request.method == 'POST':
#         new_title = request.form['title']
#         if not new_title:
#             error = "Please enter a title." #TODO make flash for error
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
