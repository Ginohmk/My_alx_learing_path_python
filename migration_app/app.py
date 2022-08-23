from tabnanny import check
from typing import final
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
import sys


# INstantiation
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setting configuration variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mike-savy:dreamlife!@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PYTHONUNBUFFERED'] = ""

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer , primary_key = True)
    description = db.Column(db.String(), nullable = False, )
    completed = db.Column(db.Boolean, nullable = False , default= False )
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False )

    def __repr__(self):
        return f'< ID: {self.id}, DESCRIP: {self.description} >'

# Parent
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    completed =db.Column(db.Boolean, nullable = False, default = False) 
    todos = db.relationship('Todo', backref ='list', lazy = True, cascade = 'all, delete-orphan')

# db.create_all()

@app.route('/todos/create', methods=['POST'])


def create_todo():
    error = False
    body = {}
    try:
      # description = request.form.get('description', '')
      description = request.get_json()['description']
      todo = Todo(description=description)
      db.session.add(todo)
      db.session.commit()
      body['description'] = todo.description
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if not error:
      # return redirect(url_for('index'))
      return jsonify({
        'description':todo.description
      })


@app.route('/todos/<todo_id>/set_completed', methods = ['POST'])

def set_completed_todo(todo_id):
    try:
      completed = request.get_json()['completed']
      print(completed)
      todo = Todo.query.get(todo_id)
      todo.completed = completed
      db.session.commit()    
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/delete', methods= ['POST'])
def delete_todo():
    try:
      todo_id = request.get_json()['id']
      todo = Todo.query.get(todo_id)
      db.session.delete(todo)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
      return jsonify({ 'success': True })



# List of todos route
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
        return render_template('index.html', 
        lists = TodoList.query.order_by('id').all(),
        active_list = TodoList.query.get(list_id),
        todos = Todo.query.filter_by(list_id = list_id).order_by('id').all())



# Create new List
@app.route('/lists/create', methods = ['POST'])

def create_list():
        body = {}
        error = False
        try:
            list = request.get_json()['newList']
            newList = TodoList(name = list)
            db.session.add(newList)
            db.session.commit()
            body['name'] = newList.name
            body['id'] = newList.id
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
            if not error:
                return jsonify({
            'name':newList.name,
            'id': newList.id
            })
# Delete list
@app.route('/delete_list', methods=['POST'] )
def delete_list():
        try:
            list_id = request.get_json()['id']
            list = TodoList.query.get(list_id)
            db.session.delete(list)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({ 'success': True })

@app.route('/update_list', methods = ['POST'] )

def update_list():
    body = {}  
    try:
        completed = request.get_json()['completed']
        list_id = request.get_json()['id']
        todo_list = TodoList.query.get(list_id)
        todo_list.completed = completed
        print(completed)
        todos_list = Todo.query.filter_by(list_id = todo_list.id)
        if completed:
                for t in todos_list:
                        print(t.description)
                        t.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify({ 'success':True})
                        

                



# Set route
@app.route('/')
# Route handler
def index():
    return redirect(url_for('get_list_todos', list_id = 1))
    # render_template('index.html', data = Todo.query.order_by('id').all())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')