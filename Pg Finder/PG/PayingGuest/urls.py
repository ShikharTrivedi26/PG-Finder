from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('addpg/',PgView.as_view(),name='addpg'),
    path('addpgdetail/',PgDetailView.as_view(),name='addpgdetail'),
    path('PGlist/',PGListView.as_view(),name='PGlist'),
    path('PGDelete/<int:pk>',PGDeleteView.as_view(),name='PGdelete'),
    path('PGUpdate/<int:pk>',PGUpdateView.as_view(),name='PGupdate'),
    path('OwnerRegister/',OwnerDashboardView.as_view(),name='OwnerDB'),
    path('RenterDashboard/',RenterDashboardView.as_view(),name='RenterDB'),
    path('PGUpdateDetail/<int:pk>',PGDetailsUpdateView.as_view(),name='PGupdateDetail'),
    path('PGDetail/<int:pk>',PGDetailsView.as_view(),name='PGDetail'),    
    path('OwnerProfile/<int:pk>',OwnerProfileView.as_view(),name='OwnerProfile'),
    path('RenterProfile/<int:pk>',RenterProfileView.as_view(),name='RenterProfile'),
    path('RenterProfileEdit/<int:pk>',RProfileUpdateView.as_view(),name='RPE'),
    path('OwnerProfileEdit/<int:pk>',OProfileUpdateView.as_view(),name='OPE'),
]