from flask_app.config.mysqlconnection import connectToMySQL
import re	
from flask import flash
from flask_app.models.post import Post

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('medemo').query_db(query,data)

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('medemo').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('medemo').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_with_posts(cls, data ):
        query = "SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('medemo').query_db(query,data)
        user = cls(results[0])
        for row in results:
            n = {
                'id': row['posts.id'],
                "quote": row["quote"],
                "date": row["date"],
                "emotion": row["emotion"],
                "content": row["content"],
                'created_at': row['posts.created_at'],
                'updated_at': row['posts.updated_at']
            }
            user.posts.append( Post(n) )
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('medemo').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "error")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters", "error")
            is_valid=False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters", "error")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "error")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "error")
            is_valid=False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match!", "error")
            is_valid=False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 5:
            flash("Email cannot be blank", "error")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "error")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "error")
            is_valid=False
        return is_valid