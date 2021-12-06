from flask import render_template, request, redirect, session, flash
from requests.api import get
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from inspire import get_random_quote
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/posts/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    quote = get_random_quote()
    return render_template("new_post.html", user=User.get_user(data), quote=quote)

@app.route('/posts/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/posts/new')
    data = {
        "quote": request.form["quote"],
        "date": request.form["date"],
        "emotion": request.form["emotion"],
        "content": request.form["content"],
        "user_id": session["user_id"]
    }
    Post.save(data)
    return redirect ('/dashboard')

@app.route('/posts/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    user_data ={
        "id" : session['user_id']
    }
    quote = get_random_quote()
    return render_template("edit_post.html",post=Post.get_one(data), user=User.get_user(user_data))

@app.route('/posts/update',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/posts/create')
    data = {
        "quote": request.form["quote"],
        "date": request.form["date"],
        "emotion": request.form["emotion"],
        "content": request.form["content"],
        "id": request.form["id"]
    }
    Post.update(data)
    return redirect('/dashboard')

@app.route('/posts/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Post.destroy(data)
    return redirect('/dashboard')
