from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1600))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods =['POST','GET'])
def index():


    blog_posts = Blog.query.all()
    return render_template('blog.html', title="Build A Blog", blog_posts=blog_posts)
        
@app.route('/newpost', methods = ['POST','GET'])
def newposts():
    
    if request.method == 'POST':
        title_name = request.form['blog_title']
        blog_post = request.form['blog_post']
        title_error = ''
        post_error = ''

        if len(title_name) == 0:
            title_error = 'You must have a title!'
    
        if len(blog_post) == 0:
            post_error = 'You must enter text for your blog post!'
        
        if not title_error and not post_error:

            new_post = Blog(title_name, blog_post)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('newpost.html', title="Add Blog Entry", 
            title_name=title_name,title_error=title_error, 
            blog_post=blog_post, post_error=post_error)
    else:
        return render_template('newpost.html', title="Add Blog Entry")


if __name__ == '__main__':
    app.run()