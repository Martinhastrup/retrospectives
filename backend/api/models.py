from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom user model for the retrospective tool."""
    email = models.EmailField(unique=True)
    userfullname = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=255, blank=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'userfullname']
    
    def __str__(self):
        return self.email


class Team(models.Model):
    """Team model for organizing users."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Retrospective(models.Model):
    """Retrospective session model."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='retrospectives', null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='retrospectives_created')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class RetrospectiveItem(models.Model):
    """Individual items in a retrospective."""
    CATEGORY_CHOICES = [
        ('start', 'Start'),
        ('stop', 'Stop'),
        ('god', 'God'),
        ('bad', 'Bad'),
        ('actions', 'Actions'),
    ]
    
    retrospective = models.ForeignKey(Retrospective, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cluster_id = models.IntegerField(default=0, help_text="Cluster ID")
    x_minimized = models.IntegerField(default=0, help_text="X coordinate for minimized square")
    y_minimized = models.IntegerField(default=0, help_text="Y coordinate for minimized square")
    x_maximized = models.IntegerField(default=0, help_text="X coordinate for maximized square")
    y_maximized = models.IntegerField(default=0, help_text="Y coordinate for maximized square")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.category}: {self.content[:50]}"


class ActionItem(models.Model):
    """Action items from retrospectives."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    retrospective = models.ForeignKey(Retrospective, on_delete=models.CASCADE, related_name='action_items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_action_items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title 