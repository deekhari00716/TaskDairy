from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):

    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    #to create relationship b/w user and todo we use foreignkeyfiels
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #this function will help to show the title of the object in databases
    def __str__(self):
        return self.title
