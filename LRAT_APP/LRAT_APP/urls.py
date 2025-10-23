from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from DATABASE_APP import views as db_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.rootPage),
    path('settings/',views.settings),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('software/', db_views.software_list, name='software_list'),
]

# use for development to load static files without restarting
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


