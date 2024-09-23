from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    title = models.CharField(max_length=25)
    date = models.DateField()
    location = models.TextField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title
   
class Customer_page(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buy_ticket = models.BooleanField(default=False)
    completed = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.customer.user.username} - {self.event.name} - {'Completed' if self.completed else 'In Progress'}"
