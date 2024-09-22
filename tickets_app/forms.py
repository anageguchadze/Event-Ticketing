from django import forms
from .models import User, Event, Customer_page

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description', 'price', 'quantity']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer_page
        fields = ['customer', 'event', 'buy_ticket', 'completed']