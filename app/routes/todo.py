from flask_restx import fields, Resource, Namespace
from TodoDAO import TodoDAO

api = Namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})

DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})

@api.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new todo'''
    @api.marshal_list_with(todo)
    def get(self):
        '''List all todos'''
        return DAO.todos

    @api.expect(todo)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a new todo'''
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        todo = DAO.get(id)
        if todo is None:
            return api.abort(404, "Todo {} doesn't exist".format(id))
        return DAO.get(id)

    @api.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a todo given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(todo)
    @api.marshal_with(todo)
    def put(self, id):
        '''Update a todo given its identifier'''
        return DAO.update(id, api.payload)