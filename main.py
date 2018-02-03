from flask import Flask, request, request, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Cdqm7kZt3c4d'




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


class User(db.Model):  # database model for users

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def must_login():
    require_login = ['newpost', "logout"]
    if request.endpoint in require_login and 'username' not in session:
        return redirect('login')

#function to validate input and length 
def validate(form_input):
    form_value = form_input
    error = ''
    if not form_input:
        error = "Why you no enter {name} !?"

    elif len(form_value) < 3 or len(form_value) > 20:  # check for length
        error = "I need something between (3-20) characters"

    elif " " in form_value:  # check for spaces
        error = "Me no likey {name} with spaces"
    return error

@app.route('/')  # route or home page displaying all users
def index():
    users = User.query.order_by(User.username.desc()).all()
    return render_template('index.html', users = users)


@app.route('/signup', methods=['GET', 'POST'])  # route to registration page
def signup():
    # if user submits form pull input from form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        user_name_error = ""
        password_error = ""
        verify_pass_error = ""
        compare_pass_error = ""
        error = "is-invalid"

        # #checks for validation of username, password, and verify password
        user_name_error = validate(username).format(name="Username")
        password_error = validate(password).format(name="Password")
        verify_pass_error = validate(
            verify_password).format(name="Verify Password")

        # #compare password to verify password
        if verify_password not in password:
            compare_pass_error = "NONE SHALL PASS!...Without matching passwords"

        #checks for empty error messages if there are no errors validation passes can move on to checking db for user
        if not (user_name_error or
                password_error or
                verify_pass_error or
                compare_pass_error
                ):
            #Check if user exists in db
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:  # make a new user if not existing
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('newpost')
            else:
                flash('User already exists, please log in', 'text-danger')
                return redirect('login')
        return render_template('signup.html',
                               username_error=user_name_error,
                               password_error=password_error,
                               verify_pass_error=verify_pass_error,
                               compare_pass_error=compare_pass_error,
                               username=username, error=error
                               )
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #if the user logs in check db for presence of username
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Username does not exist', 'text-danger')
            return render_template('login.html')
        if user.password != password:
            flash('Password is incorrect', 'text-danger')
            return render_template('login.html')

        if user and user.password == password:
            session['username'] = username
            return redirect('newpost')
    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    flash('You were successfully logged out', 'text-success')
    return redirect('/everyone')


@app.route('/singlepost')
def post():
    post_id= request.args.get('id')
    if post_id:
        new_post = Blog.query.filter_by(id= post_id).first_or_404()
        return render_template('showcase.html', new_post=new_post)
    else:
        return redirect('/everyone')


@app.route('/userpost')
def show_upost():
    selected_user= request.args.get('username')
    is_user= User.query.filter_by(username=selected_user).first()
    owner = User.query.filter_by(username=session['username']).first()
    if is_user:
        submitted_post = Blog.query.filter_by(owner=is_user).all()
        return render_template('userpost.html', submitted_post=submitted_post)

    submitted_post = Blog.query.filter_by(owner=owner).all()
    return render_template('userpost.html', submitted_post=submitted_post)


    




@app.route('/everyone')
def show_allpost():
    current_posts = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('allpost.html', current_posts=current_posts)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        new_title = request.form['title']
        if not new_title:
            error = "Please enter a title."
            return render_template('newpost.html', error=error)

        new_subtitle = request.form['subtitle']
        new_content = request.form['content']
        date = datetime.now()
        new_post = Blog(new_title, new_subtitle, date, new_content, owner)
        db.session.add(new_post)
        db.session.commit()
        post_id= new_post.id
        return redirect('/singlepost?id={}'.format(post_id))

    return render_template('newpost.html')



if __name__ == '__main__':
    app.run()


