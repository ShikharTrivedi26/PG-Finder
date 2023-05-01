from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings

app_name = 'User'

urlpatterns = [
   
 
 path('Ownerregister/',OwnerRegisterView.as_view(),name='Ownerregister'),
 path('Renterregister/',RenterRegisterView.as_view(),name='Renterregister'),
 path('login/',UserLoginView.as_view(),name='login'),
 path('logout/',LogoutView.as_view(next_page='/'),name='logout'),
 path('chat2/<int:chat_id>/', ChatView2.as_view(), name='chat2'),
#  path('chat/<int:user_id>/',ChatView.as_view(), name='chat'),
#  path('renterchat/<int:user_id>/',ChatView.as_view(), name='renterchat'),
 path('inbox/', InboxView.as_view(), name='inbox'),
 path('chat/<int:user_id>/', ChatInboxView.as_view(), name='chat'),
 
     
 
]

