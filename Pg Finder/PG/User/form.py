from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *

class RenterRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','age','gender','Phone_Number')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_renter = True
        user.save()
        return user    


class OwnerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','age','gender','PancardNo','PancardFile','AadharNo','AadharFile','Photo','Phone_Number','Address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()
        return user 
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        