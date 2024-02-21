from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs={'placeholder' : 'Enter your First Name'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'placeholder' : 'Enter your Last Name'}))
    username = forms.CharField(widget = forms.EmailInput(attrs={'placeholder' : 'Enter your Email Address'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder' : 'Enter your Password'}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder' : 'Confirm Password'}))
    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'password1', 'password2')

        labels = {
        'username': 'Email Address',
        'password1':'Password',
        'password2':'Confirm Password'
        }
        
        error_messages = {
            'username': {
                'unique': 'User with that Email Address already Exists!!',
            },
        }        

class CustomerForm(forms.ModelForm):
    phone_number = forms.CharField(widget = forms.TextInput(attrs={'placeholder' : 'Enter your Phone Number'}))
    address = forms.CharField(widget = forms.TextInput(attrs={'placeholder' : 'Enter your Address'}))
    class Meta():
        model = Customer
        fields = [
            'phone_number',
            'address'
        ]

class PaymentForm(forms.Form):
    try:
        plans = Plan.objects.all()
        plan_list = []
        for plan in plans:
            plan_sample = (plan.id, plan.name)
            plan_list.append(plan_sample)
    except:
        plan_list=[]

    plan = forms.ChoiceField(label='', choices=plan_list, required=True)
    
    class Meta:
        labels = {
            'plans' : ''
        }