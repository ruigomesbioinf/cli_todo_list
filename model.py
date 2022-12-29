# file to build our model class

import datetime

class Todo:
    def __init__(self, 
                 task: str, 
                 category: str,
                 date_added: str = None,
                 date_completed: str = None,
                 status: int = None,
                 position: int = None):
        """
        Initialize a task with the relative information.

        Args:
            task (str): Description of the task
            category (str): Category of the task
            date_added (str, optional): The date in which the task was added. Defaults to None.
            date_completed (str, optional): The date in which the task was completed. Defaults to None.
            status (int, optional): The status of the task. Completed or not completed. Defaults to None.
            position (int, optional): The position of the task. Defaults to None.
        """
        self.task = task
        self.category = category
        self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 1 # 1 = not completed, 2 = completed
        self.position = position if position is not None else None
        
    def __repr__(self) -> str:
        return f"{self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position}"