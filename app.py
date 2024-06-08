from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'a@qwerqtycvbnm'


# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flaskdb'
}

def get_db_connection():
    '''
    Function to establish a connection to the database.
    '''
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    '''
    Function to render the index.html template and display the tasks by querying the database.
    '''
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return render_template('index.html', tasks=tasks)
    except Error as e:
        flash(f"Error retrieving tasks: {e}")
        return render_template('index.html', tasks=[])
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/add_task', methods=['POST'])
def add_task():
    unique_id = request.form['unique_id']
    title = request.form['title']
    description = request.form['description']
    task_done = 'task_done' in request.form

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (unique_id, title, description, task_done) VALUES (%s, %s, %s, %s)",
            (unique_id, title, description, task_done)
        )
        connection.commit()
        flash('Task added successfully!')
    except Error as e:
        flash(f"Error adding task: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

@app.route('/update_task', methods=['POST'])
def update_task():
    unique_id = request.form['unique_id']
    title = request.form['title']
    description = request.form['description']
    task_done = 'task_done' in request.form

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE tasks SET title = %s, description = %s, task_done = %s WHERE unique_id = %s",
            (title, description, task_done, unique_id)
        )
        connection.commit()
        flash('Task updated successfully!')
    except Error as e:
        flash(f"Error updating task: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

@app.route('/delete_task/<unique_id>', methods=['GET'])
def delete_task(unique_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE unique_id = %s", (unique_id,))
        connection.commit()
        flash('Task deleted successfully!')
    except Error as e:
        flash(f"Error deleting task: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)