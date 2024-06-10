from django.contrib import admin
from django.urls import path
from django.urls import path,include
from myproject import settings
from django.conf.urls.static import static
from . import views
app_name='iot'

urlpatterns = [
    
    
   
   path('user/register/', views.user_register, name='user_register'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),

    # Home
    path('home/add_room/', views.add_room, name='add_room'),
    path('home/add_appliance/<int:room_id>', views.add_homeappliances, name='add_homeappliances'),
    path('home/get_home_appliances/', views.gethomeappliances, name='get_home_appliances'),
    path('appliances/room/<int:room_id>', views.get_appliance_details_by_room_id, name='get_appliance_details_by_room_id'),
    path('home/get_room/<int:room_id>', views.get_room_by_id, name='get_room_by_id'),
    path('home/delete_room/<int:id>/', views.delete_homeroom, name='delete_homeroom'),
    path('home/delete_appliance/<int:id>', views.delete_home_appliance, name='delete_home_appliance'),
    path('home/update_room/<int:id>', views.update_home_room, name='update_home_room'),
    path('home/update_appliance/<int:id>', views.update_home_appliance, name='update_home_appliance'),
    path('home/appliance_status/create/<int:home_id>/<int:appliance_id>/', views.create_home_appliance_status, name='create_home_appliance_status'),
    path('home/appliance_status/<int:status_id>/', views.get_home_appliance_status, name='get_home_appliance_status'),
    # path('home/appliance_status/update/<int:status_id>/', views.update_home_appliance_status, name='update_home_appliance_status'),
    path('home/appliance_status/delete/<int:status_id>/', views.delete_home_appliance_status, name='delete_home_appliance_status'),

    # Office 
    path('office/add_room/', views.add_officeroom, name='add_officeroom'),
    path('appliances/office_room/<int:room_id>', views.get_office_details_by_office_id, name='get_appliance_details_by_room_id'),
    path('office/add_appliance/<int:officeroom_id>', views.add_officeappliances, name='add_office_appliance'),
    path('office/get_office_appliances/', views.getofficeappliances, name='get_office_appliances'),
    path('office/<int:room_id>', views.get_office_details_by_office_id, name='get_office_details_by_office_id'),
    path('office/get_room/<int:room_id>', views.get_office_room_by_id, name='get_office_room_by_id'),
    path('office/delete_room/<int:id>/', views.delete_office_room, name='delete_office_room'),
    path('office/delete_appliance/<int:id>', views.delete_office_appliance, name='delete_office_appliance'),
    path('office/update_room/<int:id>', views.update_office, name='update_office'),
    path('office/update_appliance/<int:id>', views.update_officeappliance, name='update_officeappliance'),
    path('office/appliance_status/create/<int:office_id>/<int:appliance_id>/', views.create_office_appliance_status, name='create_office_appliance_status'),
    path('office/appliance_status/<int:status_id>/', views.get_office_appliance_status, name='get_office_appliance_status'),
    # path('office/appliance_status/update/<int:status_id>/', views.update_office_appliance_status, name='update_office_appliance_status'),
    path('office/appliance_status/delete/<int:status_id>/', views.delete_office_appliance_status, name='delete_office_appliance_status'),

    # MQTT
    path('mqtt/receive_status/<int:user_id>/', views.receive_status, name='receive_status'),


   

]
   
    


   

