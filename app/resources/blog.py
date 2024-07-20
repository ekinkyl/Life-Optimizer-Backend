# app/resources/blog.py

from flask_restful import Resource, reqparse
from app import mongo

# Parser for adding a new blog post
blog_post_parser = reqparse.RequestParser()
blog_post_parser.add_argument('title', type=str, required=True, help="Title cannot be blank!")
blog_post_parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")
blog_post_parser.add_argument('topic', type=str, required=True, help="Topic cannot be blank!")

# Parser for user preferences
user_pref_parser = reqparse.RequestParser()
user_pref_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
user_pref_parser.add_argument('topics', type=str, action='append', required=True, help="Topics cannot be blank!")

class BlogPostResource(Resource):
    def get(self): #Fetches all blog posts from the database.
        blog_posts = mongo.db.blog_posts.find()
        return [{'id': str(post['_id']), 'title': post['title'], 'content': post['content'], 'topic': post['topic']} for post in blog_posts]

    def post(self): #Adds a new blog post to the database.
        args = blog_post_parser.parse_args()
        blog_post = {
            "title": args['title'],
            "content": args['content'],
            "topic": args['topic']
        }
        result = mongo.db.blog_posts.insert_one(blog_post)
        return {'id': str(result.inserted_id), 'title': blog_post['title'], 'content': blog_post['content'], 'topic': blog_post['topic']}, 201

class UserPreferencesResource(Resource):
    def post(self): #Adds or updates user preferences in the database.
        args = user_pref_parser.parse_args()
        user_pref = {
            "user_id": args['user_id'],
            "topics": args['topics']
        }
        result = mongo.db.user_preferences.insert_one(user_pref)
        return {'id': str(result.inserted_id), 'user_id': user_pref['user_id'], 'topics': user_pref['topics']}, 201

    def get(self, user_id): #Fetches user preferences based on the user ID.
        user_pref = mongo.db.user_preferences.find_one({'user_id': user_id})
        if not user_pref:
            return {'message': 'User preferences not found'}, 404
        return {'user_id': user_pref['user_id'], 'topics': user_pref['topics']}

class BlogSuggestionsResource(Resource): #Provides blog post suggestions based on user preferences.
    def get(self, user_id):
        user_pref = mongo.db.user_preferences.find_one({'user_id': user_id})
        if not user_pref:
            return {'message': 'User preferences not found'}, 404
        topics = user_pref['topics']
        suggestions = mongo.db.blog_posts.find({'topic': {'$in': topics}})
        return [{'id': str(post['_id']), 'title': post['title'], 'content': post['content'], 'topic': post['topic']} for post in suggestions]
