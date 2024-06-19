from django import forms
from task_manager_app.models import TaskList

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']