from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.quote = data['quote']
        self.date = data['date']
        self.emotion = data['emotion']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (quote, date, emotion, content, user_id) VALUES (%(quote)s, NOW(), %(emotion)s, %(content)s, %(user_id)s);"
        return connectToMySQL('medemo').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        result = connectToMySQL('medemo').query_db(query)
        posts = []
        for u in posts:
            posts.append( cls(u) )
        return posts

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL('medemo').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE posts SET date=NOW(),emotion=%(emotion)s,content=%(content)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('medemo').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('medemo').query_db(query,data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['emotion']) < 1:
            flash("You must choose an emotion!", "error")
            is_valid=False
        if len(post['content']) < 3:
            flash("Diary entry must be at least 3 characters", "error")
            is_valid=False
        return is_valid



