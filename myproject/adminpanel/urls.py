from django.contrib import admin
from django.urls import path
from adminpanel import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'adminpanel1'

urlpatterns = [
    path('adminpanel/api/adminlogin', csrf_exempt(views.admin_login), name='admin_login'),
    path('adminpanel/api/getrooms', csrf_exempt(views.get_rooms_of_all), name='getrooms'),
    path('adminpanel/api/gethomeappliance', csrf_exempt(views.get_homeappliance_of_all), name='gethomeappliance'),
    path('adminpanel/api/getofficerooms', csrf_exempt(views.get_officerooms_of_all), name='getofficerooms'),
    path('adminpanel/api/getofficeappliance', csrf_exempt(views.get_officeappliance_of_all), name='getofficeappliance'),
    path('adminpanel/api/userdetails/<int:id>', csrf_exempt(views.userdetails), name='userdetails'),
    path('rooms/<int:id>/', csrf_exempt(views.get_room_details_id), name='get_room_details'),
    path('homeappliance/<int:id>/', csrf_exempt(views.get_homeappliance_details_id), name='get_homeappliance_details'),
    path('api/users/details/', csrf_exempt(views.get_all_users_details), name='get_all_users_details'),
]
