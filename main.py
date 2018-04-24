from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'jfjfjfjfjfj'

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





#@app.before_request
#def require_login():
 #   allowed_routes = ['login', 'signup', 'index']
  #  if request.endpoint not in allowed_routes and 'username' not in session:
    
   #     return redirect('/login')
   #this somehow disabled css... Also didn't work correctly


@app.route('/')
def blog_index():
    return redirect('/index')


@app.route('/signup', methods=['POST', 'GET'])
def signup():


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pass = request.form['verify-pass']

        username_error = ''
        password_error = ''
        verify_error = ''
        
        if (not username) or (username.strip() == '') or ((len(username) > 20 or len(username) < 3)) or (' ' in username):
            username_error = "That's not a valid username"
            username = ''

        if (not password) or (password.strip() == '') or ((len(password) > 20 or len(password) < 3)) or (' ' in password):
            password_error = "That's not a valid password"

        if (password != verify_pass) or (not verify_pass):
            verify_error = "Passwords don't match"


        existing_user = User.query.filter_by(username=username).first()
        if (not username_error) and (not password_error) and (not verify_error):
            
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username']= username
            
                return redirect ('/newpost?username={0}'.format(username))
        else:
            return render_template('signup.html', username_error=username_error,
                    password_error=password_error, verify_error=verify_error)
    else:
   
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('logged in')
            return redirect('/newpost?username={0}'.format(username)) #think about maybe formating this to user.id ??
        else:
            flash('username or password incorrect') #need to fix this to make sure flash is working

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/index', methods=['GET', 'POST'])
def index():

        if request.args.get('id'):
            blog_id = request.args.get('id')
            blog = Blog.query.get(blog_id)
            return render_template('allposts.html', blog = blog)

    
        users = User.query.all()
        return render_template('index.html', users = users)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()
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
            new_post = Blog(blog_title, blog_body, owner)
            db.session.add(new_post)
            db.session.commit()

        
            return redirect('/index?id={0}'.format(new_post.id))
        else:
            return render_template('newpost.html', title_error = title_error, body_error = body_error )

    #else:
    return render_template('newpost.html')

@app.route('/singleUser')
def single_user():
    #TODO add functionality to display a single user and their corresponding blog posts
    return render_template('singleUser.html')

@app.route('/allposts')
def all_posts():
    #TODO add functionality to display all users and their corresponding blog posts
    return render_template('allposts.html')



if __name__ == '__main__':
    app.run()