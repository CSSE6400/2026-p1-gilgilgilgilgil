from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api/v1')

# In-memory store
todos = {}
counter = 1

ALLOWED_FIELDS = {'title', 'description', 'completed', 'deadline_at'}


# GET /api/v1/health
@api.route('/health')
def health():
    return jsonify({"status": "ok"})


# GET /api/v1/todos
@api.route('/todos', methods=['GET'])
def get_todos():
    completed_param = request.args.get('completed')
    window_param = request.args.get('window')

    result = list(todos.values())

    # Filter by completed status
    if completed_param is not None:
        if completed_param.lower() == 'true':
            result = [t for t in result if t['completed'] is True]
        elif completed_param.lower() == 'false':
            result = [t for t in result if t['completed'] is False]

    # Filter by window (tasks due within N days from today)
    if window_param is not None:
        try:
            window = int(window_param)
            cutoff = datetime.utcnow() + timedelta(days=window)
            filtered = []
            for t in result:
                if t.get('deadline_at'):
                    deadline = datetime.fromisoformat(t['deadline_at'])
                    if deadline <= cutoff:
                        filtered.append(t)
            result = filtered
        except ValueError:
            return jsonify({"error": "window must be an integer"}), 400

    return jsonify(result)


# GET /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    if id not in todos:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todos[id])


# POST /api/v1/todos
@api.route('/todos', methods=['POST'])
def create_todo():
    global counter
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "title is required"}), 400

    # Reject unknown fields
    extra_fields = set(data.keys()) - ALLOWED_FIELDS
    if extra_fields:
        return jsonify({"error": f"Unknown fields: {extra_fields}"}), 400

    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    new_todo = {
        "id": counter,
        "title": data['title'],
        "description": data.get('description', None),
        "completed": data.get('completed', False),
        "deadline_at": data.get('deadline_at', None),
        "created_at": now,
        "updated_at": now,
    }
    todos[counter] = new_todo
    counter += 1
    return jsonify(new_todo), 201


# PUT /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    if id not in todos:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()

    # Reject unknown fields
    extra_fields = set(data.keys()) - ALLOWED_FIELDS
    if extra_fields:
        return jsonify({"error": f"Unknown fields: {extra_fields}"}), 400

    todo = todos[id]
    if 'title' in data:
        todo['title'] = data['title']
    if 'description' in data:
        todo['description'] = data['description']
    if 'completed' in data:
        todo['completed'] = data['completed']
    if 'deadline_at' in data:
        todo['deadline_at'] = data['deadline_at']

    todo['updated_at'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    return jsonify(todo)


# DELETE /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    # Spec says return 200 with empty response if not found
    if id not in todos:
        return jsonify({}), 200
    todo = todos.pop(id)
    return jsonify(todo), 200