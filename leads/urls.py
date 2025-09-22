from django.contrib import admin
from django.urls import path
from . import views
app_name= "leads"

urlpatterns=[ 
             #name is used for dynamic change of url name
      path('all/',views.LeadListView.as_view(), name='lead-list'),
      path('create/',views.LeadCreateView.as_view(), name='lead-create'),
      path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
      path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
      path('<int:pk>/', views.LeadDetailView.as_view(), name='lead-details'),
      
]