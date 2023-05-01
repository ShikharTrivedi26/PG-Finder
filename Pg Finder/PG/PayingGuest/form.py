from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import PG,PG_details

class AddPGform(forms.ModelForm):
    class Meta():
        model=PG
        fields=('user','name','gender','rooms','room_sharing','price','pg_addres')
    
class AddPGdetailsform(forms.ModelForm):
    class Meta():
        model=PG_details
        fields=('user','no_of_cupboard','no_of_beds','pg_type','pgdetails_id','pg_image','desc','area','near_by_place')
