from django.contrib import admin
from django.urls import path
from . import views
app_name= "leads"

urlpatterns=[ 
             #name is used for dynamic change of url name
   path('all/',views.lead_list, name='lead-list'),
   path('create/',views.lead_create, name='lead-create'),
   path('<int:pk>/update/', views.lead_update, name='lead-update'),
   path('<int:pk>/delete/', views.lead_delete, name='lead-delete'),
   path('<int:pk>/', views.lead_detail, name='lead-details'),
   
]