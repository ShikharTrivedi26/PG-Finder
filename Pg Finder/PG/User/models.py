from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Gender=(("Male","Male"),("Female","Female"),("Others","Others"))
class User(AbstractUser):
    is_owner=models.BooleanField(default=False)
    is_renter=models.BooleanField(default=False)
    age=models.IntegerField(default=0)
    gender=models.CharField(choices=Gender,max_length=20)
    AadharNo=models.IntegerField(default=0)
    AadharFile=models.FileField(upload_to='aadharFile/')
    PancardNo=models.IntegerField(default=0)
    PancardFile=models.FileField(upload_to='Panfile/')
    Photo=models.ImageField(upload_to='Photo/')
    Phone_Number=models.CharField(max_length=12 ,null=True)
    Address=models.TextField(max_length=5000 ,null=True)
    class Meta:
        db_table='User'
        
class Chat(models.Model):
    owner = models.ForeignKey(User, related_name='owner_chats', on_delete=models.CASCADE)
    renter = models.ForeignKey(User, related_name='renter_chats', on_delete=models.CASCADE)
    messages = models.TextField(blank=True)

    def __str__(self):
        return f'Chat between {self.owner.username} and {self.renter.username}'        
        
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='Message'
    

    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.content}'    

       