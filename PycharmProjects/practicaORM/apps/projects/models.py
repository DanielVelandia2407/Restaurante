from django.db import models
from apps.users.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    init_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

PRIORITY_CHOICES = (
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High')
)
class Task(models.Model):
    description = models.CharField(max_length=250, null=False, blank=False)
    end_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    priority = models.CharField(max_length=60, choices=PRIORITY_CHOICES, default='LOW')

class Comment(models.Model):
    init_date = models.DateTimeField()
    content = models.CharField(max_length=120)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

ROLE_CHOICES = (
    ('DEV', 'Developer'),
    ('PO', 'Product Owner'),
    ('SM', 'Scrum Master'),
    ('QA', 'Quality Assurance')
)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=60, choices=ROLE_CHOICES)
    date = models.DateTimeField()

class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
