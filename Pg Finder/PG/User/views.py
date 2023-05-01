from django.shortcuts import render
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from .models import *
from .form import RenterRegisterForm,OwnerRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .form import *
from .models import Chat
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic import View
from django.forms.models import modelform_factory
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your models here.
class RenterRegisterView(CreateView):
    model = User
    form_class = RenterRegisterForm
    template_name = 'User/Renter_register.html'
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'renter'
        return super().get_context_data(**kwargs)
    
    def form_valid(self,form):
        #email = form.cleaned_data.get('email')
        user = form.save()
        login(self.request,user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)
    
    def send_welcome_email(self,user_email):
        subject = 'Welcome to our site!'
        message = 'Renter Register success'
        from_email = 'django@gmail.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

class OwnerRegisterView(CreateView):
    model = User
    form_class = OwnerRegistrationForm
    template_name = 'User/owner_register.html'
    success_url = "/"    
    
    def form_valid(self,form):
        #email = form.cleaned_data.get('email')
        user = form.save()
        login(self.request,user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)
    
    def send_welcome_email(self,user_email):
        subject = 'Welcome to our site!'
        message = ' Register(Owner) success'
        from_email = 'django@gmail.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class UserLoginView(LoginView):
    template_name = 'User/login.html'
    success_url = "/"
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_renter:
             return '../../PayingGuest/RenterDashboard/'
            else:
             return '../../PayingGuest/OwnerRegister/'
         
def home(request):
    return render(request,'User/Dashboard.html')    


class ChatView2(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'chat2.html'
    model = Chat
    
    ordering = ['id']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user) | qs.filter(renter=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, pk=chat_id)
        context['chat'] = chat
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, pk=chat_id)
        message = form.cleaned_data.get('message')
        chat.messages += f"{self.request.user.username}: {message}\n"
        chat.save()
        return super().form_valid(form)

class InboxView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'User/inbox.html'
    context_object_name = 'PGlist'

    def get(self,request,*args,**kwargs):
       
       pg=User.objects.all().values()
       return render(request,self.template_name) 
    
# class ChatView(LoginRequiredMixin, CreateView):
#     template_name = 'User/chat.html'
#     model = Message
#     form_class = MessageForm
#     success_url = "http://127.0.0.1:8000/User/chat/3/"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         recipient = get_object_or_404(User, pk=self.kwargs['user_id'])
#         context['recipient'] = recipient
#         print(self.kwargs)  # Print the kwargs dictionary to check the value of 'pk'
#         return context

#     def form_valid(self, form):
#         recipient = get_object_or_404(User, pk=self.kwargs['user_id'])
#         form.instance.recipient = recipient
#         form.instance.sender = self.request.user
#         response = super().form_valid(form)

#         channel_layer = get_channel_layer()
#         payload = {
#             'type': 'chat_message',
#             'message': form.instance.content,
#             'user_id': str(self.request.user.id),
#         }
#         async_to_sync(channel_layer.group_send)(
#             f'chat_{recipient.id}_group',
#             payload
#         )
#         return response
    
#     def get_redirect_url(self):
#         if self.request.user.is_authenticated:
#             if self.request.user.is_renter:
#              return 'User/renterchat.html'
#             else:
#              return 'User/chat.html'

class ChatInboxView(LoginRequiredMixin, View):
    template_name = 'User/chat.html'
    MessageForm = modelform_factory(Message, fields=('content',))

    def get(self, request, user_id=None):
        if user_id is None:
            messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).distinct().order_by('-created_at')
            context = {'messages': messages}
            return render(request, self.template_name, context)
        else:
            recipient = get_object_or_404(User, pk=user_id)
            messages = Message.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)).order_by('created_at')
            form = self.MessageForm()
            context = {'recipient': recipient, 'messages': messages, 'form': form}
            return render(request, self.template_name, context)

    def post(self, request, user_id):
        recipient = get_object_or_404(User, pk=user_id)
        form = self.MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()

            channel_layer = get_channel_layer()
            payload = {
                'type': 'chat_message',
                'message': message.content,
                'user_id': str(request.user.id),
            }
            async_to_sync(channel_layer.group_send)(
                f'chat_{recipient.id}_group',
                payload
            )

            return HttpResponseRedirect(reverse('User:chat', kwargs={'user_id': user_id}))
        else:
            messages = Message.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)).order_by('created_at')
            context = {'recipient': recipient, 'messages': messages, 'form': form}
            return render(request, self.template_name, context)