from django.db import models
from django.contrib.auth.models import User

class TodoItem(models.Model):
    # Auto-incrementing primary key for each todo item
    serial_number = models.AutoField(primary_key=True, auto_created=True)

    # Title or description of the todo item
    title = models.CharField(max_length=200)

    # Automatically stores the date when the item is created
    date = models.DateField(auto_now_add=True)

    # Status of the task: False = Incomplete, True = Completed
    status = models.BooleanField(default=False)

    # Link each todo item to a specific user; 
    # if the user is deleted, all their todo items are deleted too
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_items')

    # String representation for better readability in Django admin or shell
    def __str__(self):
        return f"{self.title} - {'Completed' if self.status else 'Pending'}"
