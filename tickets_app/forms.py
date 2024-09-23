from django import forms
from .models import User, Event, Customer_page


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description', 'price', 'quantity']
    
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d', '%m.%d.%Y', '%d.%m.%Y']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer_page
        fields = ['customer', 'event', 'buy_ticket', 'completed']