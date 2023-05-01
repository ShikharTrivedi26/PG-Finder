from django.shortcuts import render
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from .models import PG,PG_details
from django.views.generic import ListView,DetailView
from .form import AddPGform,AddPGdetailsform
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from User.models import *
from User.form import *
from django.urls import reverse_lazy

class PgView(CreateView):
    model= PG
    form_class=AddPGform
    template_name='pg/registerpg.html'
    success_url='../addpgdetail/'

class PGDetailsView(DetailView):
    model= PG
    context_object_name='PGlist'
    template_name='pg/PGDetailView.html'
    
    
    def get(self,request,*args,**kwargs):
       
       pg=PG.objects.all().values('user_id')
       print("------",pg)
       pid= pg[0].get('user_id')
       pgdetails=PG_details.objects.all().values()
       print("------",pgdetails)
       return render(request,self.template_name,{'PGlist':self.get_object(),'pg':pg,'pgdetails':pgdetails}) 
   
    
class OwnerDashboardView(LoginRequiredMixin,ListView):
    model= PG
    context_object_name = 'PGlist'
    template_name='pg/OwnerDashBoardView.html'
    success_url='/OwnerDashBoardView/'
    
    def get_queryset(self):
        
       queryset = super().get_queryset()
       queryset = queryset.filter(user_id=self.request.user)
       return queryset


class PgDetailView(CreateView):
    model= PG_details
    form_class=AddPGdetailsform
    template_name='pg/addpgdetail.html'
    success_url='/PayingGuest/OwnerRegister/'

class PGListView(ListView):
    model = PG
    template_name = 'pg/PGlist.html'
    context_object_name = 'PGlist'
    
    def get_queryset(self):
        return super().get_queryset()
    
class PGDeleteView(DeleteView):
    model = PG
    template_name = 'pg/PGdelete.html'
    success_url = '/PayingGuest/PGlist'  
    
class PGUpdateView(UpdateView):
    model = PG
    template_name = 'pg/UpdatePG.html'
    fields = '__all__'
    success_url = '/PayingGuest/OwnerRegister/'     
         
class PGDetailsUpdateView(UpdateView):
    model = PG_details
    template_name = 'pg/UpdatePGdetail.html'
    fields = '__all__'
    success_url = '/PayingGuest/OwnerRegister/'     
         
class RenterDashboardView(ListView):
    model= PG
    context_object_name = 'PGlist'
    template_name='pg/RenterDashBoardView.html'
    success_url='/RenterDashBoardView/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        sort_by = self.request.GET.get('sort_by')
        
        if sort_by == 'price low-high':
            queryset = queryset.order_by('price')
        elif sort_by == 'price high-low':
            queryset = queryset.order_by('-price')    
            
        elif sort_by == 'gender':
            queryset = queryset.order_by('gender')
        elif sort_by == 'rooms':
            queryset = queryset.order_by('rooms')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['sort_options'] = [
            {'value': 'price low-high', 'label': 'Sort by Price Low-High'},
            {'value': 'price high-low', 'label': 'Sort by Price High-Low'},
            {'value': 'gender', 'label': 'Sort by Gender'},
            {'value': 'rooms', 'label': 'Sort by Rooms'},
        ]
        
        context['selected_sort_option'] = self.request.GET.get('sort_by', 'price')
        return context
    
    #def get_queryset(self):
        
       ##queryset = super().get_queryset()
       #queryset = queryset.filter(name=self.request.user)
       #return queryset
       
class OwnerProfileView(DetailView):
    model=User
    context_object_name = 'owner'
    form_class=OwnerRegistrationForm
    template_name='pg/OwnerProfile.html'
    
class RenterProfileView(DetailView):
    model=User
    context_object_name = 'renter'
    form_class=RenterRegisterForm
    template_name='pg/RenterProfile.html'
        
        
class RProfileUpdateView(UpdateView):
    model = User
    template_name = 'pg/RenterProfileEdit.html'
    form_class=RenterRegisterForm
    
    success_url = ""         
    
class OProfileUpdateView(UpdateView):
    model = User
    template_name = 'pg/OwnerProfileEdit.html'
    form_class=OwnerRegistrationForm
    
    success_url = ''             
    