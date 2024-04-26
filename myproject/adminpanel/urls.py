from django.contrib import admin
from django.urls import path, include
from myproject import settings
from django.conf.urls.static import static
from adminpanel import views

app_name = 'adminpanel1'

urlpatterns = [
    path('adminpanel/api/getrooms', views.get_rooms, name='getrooms'),
    path('adminpanel/api/gethomeappliance', views.get_homeappliance, name='gethomeappliance'),
    path('adminpanel/api/getofficerooms', views.get_officerooms, name='getofficerooms'),
    path('adminpanel/api/getofficeappliance', views.get_officeappliance, name='getofficeappliance'),
    path('adminpanel/api/adminlogin', views.admin_login, name='admin_login'),
    path('adminpanel/api/userdetails/<int:id>', views.userdetails, name='userdetails'),
]
