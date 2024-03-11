from flask import Flask
import os
from flask import redirect, url_for, jsonify, make_response, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from models import db, BlogPost
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dhh_eyeue3384743_383ht7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite::///' + os.path.join(basedir, 'flaskdb.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql:://root:root@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# route for "/"
@app.route('/')
def hello_world():
    return render_template("index.html")
    #return '<h1>Hello, World!</h2>'

@app.route('/blog')
def blog():
    blogPosts = [
        {'id':1, 'title':'First post', 'content':'Content of the first post'},
        {'id':2, 'title':'Second post', 'content':'Content of the second post'},
    ]
    return render_template("blog.html", posts=blogPosts)

# route for "/about"
@app.route('/about')
def about():
    return 'This is the about page'

# define a dynamic route for viewing blog posts by post ID
@app.route('/post/<int:post_id>')
def view_post(post_id):
    #Logic to retrieve post and display the post with the given post_id
    return f"Viewing Blog Post #{post_id}"

@app.route('/user/<username>')
def user_profile(username):
    # Logic to display user profile based on username
    return f'profile.html, {username}' 

#url = url_for('user_profile', username='alice')
#print(url)

@app.route('/api/data')
def get_data():
    data = {'key':'value'}
    return jsonify(data)

@app.route('/old-url')
def old_url():
    return redirect(url_for('user_profile', username='sodmond'))

@app.route('/set-cookie')
def set_cookie():
    response = 'Cookie Set!'
    resp = make_response(response)
    resp.set_cookie('user_id', '123')
    resp.headers['Custom-Header'] = 'Custom Value'
    return resp

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"class": "form-control"})
    body = TextAreaField('Content', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Create Post', render_kw={"class": "btn btn-primary"})

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # Process form data and create a new blog post
        post = BlogPost()
        form.populate_obj(post)
        # Perform further actions (e.g. database operations)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index')) # Redirect to the home page after creating the post
    return render_template('create_post.html', form=form)  

if __name__ == '__main__':
    app.run()