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

@app.route('/blog')
def index():
    post_id = request.args.get('id')
    if (post_id):
        ind_entry = Blog.query.get(post_id)
        return render_template('ind_entry_page.html', ind_entry=ind_entry)
    else:
        all_posts = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blog_posts=all_posts)

        
@app.route('/newpost', methods = ['POST','GET'])
def newposts():
    
    if request.method == 'POST':
        title_name = request.form['blog_title']
        blog_post = request.form['blog_post']
        title_error = ''
        post_error = ''

        if len(title_name) == 0 and len(blog_post) == 0:
            title_error = 'You must have a title!'
            post_error = 'You must enter text for your blog post!'
            
        if len(title_name) > 0 and len(blog_post) == 0:
            title_error = "You must have a title!"
            return render_template('newpost.html',title_name=title_name, title_error=title_error)
        
        if len(blog_post) > 0 and len(title_name) == 0:
            post_error = "You must enter text for your blog post!"
            return render_template('newpost.html', blog_post=blog_post, post_error=post_error)
            
        if not title_error and not post_error:

            new_post = Blog(title_name, blog_post)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_post.id))
        else:
            return render_template('newpost.html', title="Add Blog Entry", 
            title_name=title_name,title_error=title_error, 
            blog_post=blog_post, post_error=post_error)
    else:
        return render_template('newpost.html', title="Add Blog Entry")



if __name__ == '__main__':
    app.run()