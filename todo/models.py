from django.db import models
from django.contrib.auth.models import User
import uuid


class TodoList(models.Model):
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class ClassItem(models.model):
    name = models.CharField(max_length=100)
    time_start = models.TimeField()
    time_end = models.TimeField()
    location = models.CharField(max_length=100)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name