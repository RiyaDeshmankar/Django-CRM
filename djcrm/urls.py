from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path,include
from leads import views
from leads.views import SignupView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPagebView.as_view(), name='landing-page'),
    path('leads/',include('leads.urls')),
    path('agents/',include('agents.urls')),
    path('login/',LoginView.as_view(), name='login-view'),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout-view'),
    path('signup/',SignupView.as_view(), name='signup-view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    