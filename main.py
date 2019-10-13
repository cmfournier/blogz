from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1600))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Username does not exist','error')
            return render_template('login.html', title="Login")

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect or does not exist','error')

    return render_template('login.html', title="Login")

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

#verify required fields aren't empty
        if len(username) == 0:
            flash("Username cannot be blank","error")
            return render_template('signup.html', title="Sign Up")

        if len(password) == 0:
            flash("Password cannot be blank","error")
            return render_template('signup.html', title="Sign Up")

        if len(verify) == 0:
            flash("Please verify your password in the Verify field","error")
            return render_template('signup.html', title="Sign Up")

#verify username is valid length
        if len(username) < 3:
            flash("Username must be at least 3 characters long","error")
            return render_template('signup.html', title="Sign Up")

#verify password is valid length
        if len(password) < 3:
            flash("Password must be at least 3 characters long","error")
            return render_template('signup.html', title="Sign Up")

#ensure passwords match
        if password != verify:
            flash("Passwords don't match", "error")
            return render_template('signup.html', title="Sign Up")

#verify username and add to db if new
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("Username already exists", "error")
            return render_template('signup.html', title="Sign Up")
    else:
        return render_template('signup.html', title="Sign Up")

@app.route('/')
def index():
    all_users = User.query.all()
    return render_template('index.html', title="Blogz", all_users=all_users)

@app.route('/blog')
def list_blogs():
    post_id = request.args.get('id')
    user_id = request.args.get('owner_id')

    if (post_id):
        ind_entry = Blog.query.get(post_id)
        return render_template('ind_entry_page.html', title="Blogz", ind_entry=ind_entry)
    else:
        if (user_id):
            ind_user_posts = Blog.query.filter_by(owner_id=user_id)
            return render_template('ind_user_page.html', title="Blogz", posts = ind_user_posts)
        else:
            all_posts = Blog.query.all()
            return render_template('blog.html', title="Blogz", blog_posts=all_posts)

        
@app.route('/newpost', methods = ['POST','GET'])
def newposts():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title_name = request.form['blog_title']
        blog_post = request.form['blog_body']
        title_error = ''
        post_error = ''

        if len(title_name) == 0:
            title_error = "You must have a title!"
            
        if len(blog_post) == 0:
            post_error = "You must enter text for your blog post!"

        if not title_error and not post_error:

            new_post = Blog(title_name, blog_post, owner)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_post.id))
        else:
            return render_template('newpost.html', title="Add Blog Entry", 
            title_name=title_name,blog_post=blog_post, 
            title_error=title_error,post_error=post_error)
    else:
        return render_template('newpost.html', title="Add Blog Entry")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')



if __name__ == '__main__':
    app.run()