from flask import Flask
from flask_restx import Api, Resource
from routes.todo import api as todo_api

app = Flask(__name__)
api = Api(app, version='1.0', title='TodoMVC API',
    description='Simple TodoMVC API'
)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_namespace(todo_api)

if __name__ == '__main__':
    app.run(debug=True)