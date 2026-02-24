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
   return jsonify([{ 
     "id": 1, 
     "title": "Watch CSSE6400 Lecture", 
     "description": "Watch the CSSE6400 lecture on ECHO360 for week 1", 
     "completed": True, 
     "deadline_at": "2026-02-27T18:00:00", 
     "created_at": "2026-02-20T14:00:00", 
      "updated_at": "2026-02-20T14:00:00" 
    }])


# GET /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['GET']) 
def get_todo(id): 
   return jsonify({ 
     "id": id, 
     "title": "Watch CSSE6400 Lecture", 
     "description": "Watch the CSSE6400 lecture on ECHO360 for week 1", 
     "completed": True, 
     "deadline_at": "2026-02-27T18:00:00", 
     "created_at": "2026-02-20T14:00:00", 
      "updated_at": "2026-02-20T14:00:00" 
    })



# POST /api/v1/todos
@api.route('/todos', methods=['POST']) 
def create_todo(): 
   return jsonify({ 
     "id": 1, 
     "title": "Watch CSSE6400 Lecture", 
     "description": "Watch the CSSE6400 lecture on ECHO360 for week 1", 
     "completed": True, 
     "deadline_at": "2026-02-27T18:00:00", 
     "created_at": "2026-02-20T14:00:00", 
      "updated_at": "2026-02-20T14:00:00" 
    }), 201


# PUT /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['PUT']) 
def update_todo(id): 
   return jsonify({ 
     "id": id, 
     "title": "Watch CSSE6400 Lecture", 
     "description": "Watch the CSSE6400 lecture on ECHO360 for week 1", 
     "completed": True, 
     "deadline_at": "2026-02-27T18:00:00", 
     "created_at": "2026-02-20T14:00:00", 
      "updated_at": "2026-02-20T14:00:00" 
    })


# DELETE /api/v1/todos/<id>
@api.route('/todos/<int:id>', methods=['DELETE']) 
def delete_todo(id): 
   return jsonify({ 
     "id": id, 
     "title": "Watch CSSE6400 Lecture", 
     "description": "Watch the CSSE6400 lecture on ECHO360 for week 1", 
     "completed": True, 
     "deadline_at": "2026-02-27T18:00:00", 
     "created_at": "2026-02-20T14:00:00", 
      "updated_at": "2026-02-20T14:00:00" 
    })