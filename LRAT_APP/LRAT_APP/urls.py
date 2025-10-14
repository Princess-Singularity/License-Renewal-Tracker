from django.contrib import admin
from django.urls import path
from . import views  #Import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.rootPage),
    path('settings/',views.settings),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
]


