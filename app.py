from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
database = client['todolist_db']
collection = database['todolist']

@app.route('/')
def index():
    todos = list(collection.find())
    return render_template('index.html',todos = todos)

@app.route('/add',methods = ['POST'])
def add():
    todo_content = request.form['content']
    if todo_content:
        collection.insert_one({'content': todo_content,'completed':False})
        return redirect(url_for('index'))
    

@app.route('/add-subtask/<todo_id>',methods = ['POST'])
def add_subtodo(todo_id):
    subtodo_content = request.form['subtodo-content']
    if subtodo_content:
        collection.update_one({'_id': ObjectId(todo_id)},
                              {'$push':{'subtodos':{'content':subtodo_content,'completed':False}}})
        return redirect(url_for('index'))

@app.route('/update/<todo_id>',methods = ['POST'])
def update(todo_id):
    new_content = request.form['content']
    collection.update_one({'_id': ObjectId(todo_id)},{'$set':{'content':new_content,'completed':False}})
    return redirect(url_for('index'))

@app.route('/complete/<todo_id>')
def complete(todo_id):
    collection.update_one({'_id':ObjectId(todo_id)},{'$set':{'completed': True}})
    return redirect(url_for('index'))

@app.route('/incomplete/<todo_id>')
def incomplete(todo_id):
    collection.update_one({'_id':ObjectId(todo_id)},{'$set':{'completed': False}})
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>')
def delete(todo_id):

    collection.delete_one({'_id':ObjectId(todo_id)})
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)