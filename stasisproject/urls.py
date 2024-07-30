from django.contrib import admin
from django.urls import path, include
from stasisapp import views  # Import from your app, not the project

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_data, name='get_data'),  # Include views from your app
    path('get-data/', views.get_data, name='get_data')
]
