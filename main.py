from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password





@app.route('/')
def blog_index():
    return redirect('/blog')


@app.route('/index')
def index():
    return redirect('/blog')

@app.route('/signup')
def signup():
    return redirect('/blog')

@app.route('/login')
def login():
    return redirect('/blog')


@app.route('/blog', methods=['GET', 'POST'])
def blog():

        if request.args.get('id'):
            blog_id = request.args.get('id')
            blog = Blog.query.get(blog_id)
            return render_template('display.html', blog = blog)

    
        blogs = Blog.query.all()
        return render_template('blog.html', blogs = blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blog-body']
        title_error = ''
        body_error = ''

        if (blog_title.strip() == ''):
            title_error = "Please enter a title"

        
        if (blog_body.strip() == ''):
            body_error = "Please enter a blog"
            
        
    
        if not title_error and not body_error:
            #blog_title = request.form['title']
            #blog_body = request.form['blog-body']
            new_post = Blog(blog_title, blog_body, owner)
            db.session.add(new_post)
            db.session.commit()

        
            return redirect('/blog?id={0}'.format(new_post.id))
        else:
            return render_template('newpost.html', title_error = title_error, body_error = body_error )

    else:
        return render_template('newpost.html')





if __name__ == '__main__':
    app.run()