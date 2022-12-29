# file to work with sql database

import sqlite3
from typing import List
import datetime
from model import Todo

connection = sqlite3.connect("todos.db")
cursor = connection.cursor()

def create_table():
    """
    Function to create our table in SQLite3
    """
    cursor.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )""")
    
create_table()

def insert_todo(todo: Todo):
    """
    Insert todo task into the database

    Args:
        todo (Todo): Todo task
    """
    cursor.execute("SELECT COUNT(*) FROM todos") # get the number of todos in our table
    count = cursor.fetchone()[0] # get the number of items in our table
    todo.position = count if count else 0
    with connection:
        cursor.execute("INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)",
                       {"task": todo.task, "category": todo.category, "date_added": todo.date_added, "date_completed": todo.date_completed,
                        "status": todo.status, "position": todo.position})
        
def get_all_todos() -> List[Todo]:
    """
    Get all the todo tasks in the database

    Returns:
        List[Todo]: List
    """
    cursor.execute("SELECT * FROM todos")
    results = cursor.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete_todo(position):
    """
    Delete a todo task by the position index

    Args:
        position (_type_): Index of the task
    """
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]
    
    with connection:
        cursor.execute("DELETE FROM todos WHERE position=:position", 
                       {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)
            
def change_position(old_position: int, new_position: int, commit: bool = True):
    """
    Auxiliary function to change the position number of remaining tasks after the deletion of tasks

    Args:
        old_position (int): Old position index
        new_position (int): New position index
        commit (bool, optional): Boolean value to check if the changes will be commited to database or not. Defaults to True.
    """
    cursor.execute("UPDATE todos SET position = :position_new WHERE position = :position_old",
                   {"position_new": new_position, "position_old": old_position})
    
    if commit:
        connection.commit()
        
def update_todo(position: int, task: str, category:str):
    """
    Function that updates information of a todo task

    Args:
        position (int): Position index of todo task.
        task (str): Description of todo task.
        category (str): In which category the task belongs to.
    """
    with connection:
        if task is not None and category is not None:
            cursor.execute("UPDATE todos SET task = :task, category = :category WHERE position = :position",
                           {"task": task, "category": category, "position": position})
        elif task is not None:
            cursor.execute("UPDATE todos SET task = :task WHERE position = :position",
                           {"task": task, "position": position})
        elif category is not None:
            cursor.execute("UPDATE todos SET category = :category WHERE position = :position",
                           {"position": position, "category": category})
            
def complete_todo(position: int):
    """
    Function that sets a todo as completed in the database.

    Args:
        position (int): Position index of the todo task.
    """
    with connection:
        cursor.execute("UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position",
                       {"position": position, "date_completed": datetime.datetime.now().isoformat()})
        