from django.contrib import admin

from ToDoList.models import UserTB, TasksTB

# Register your models here.

admin.site.register(UserTB)
admin.site.register(TasksTB)
