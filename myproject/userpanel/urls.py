from django.contrib import admin
from django.urls import path
from django.urls import path,include
from myproject import settings
from django.conf.urls.static import static
from . import views
app_name='iot'

urlpatterns = [
    
    
   
    # path('adminpanel/api/iotusers',views.userview,name='iotusers'),
    path('api/register',views.admin_register,name='adminregister'),
    path('api/login',views.admin_login,name='adminlogin'),
    path('api/logout',views.admin_logout,name='adminlogout'),
    path('api/homeroom/add',views.add_room,name='addhomeroom'),#api to add homeroom
    path('api/homeroom/addappliance/',views.add_homeappliances,name='addhomeappliances'),#api to add appliances
    path('api/officeroom/add',views.add_officeroom,name='addofficeroom'),#to add officeroom
    path('api/officeroom/addofficeappliance',views.add_officeappliances,name='addofficeappliance'),#to add officeapplance
    #  path('adminpanel/api/getrooms', views.get_homeroom, name='getrooms'),
    path('api/roomdetails/count', views.get_room_details, name='room-details'),
    path('api/homeroom/gethomeroom',views.get_homeroom,name='gethomeroom'),#to get the data of homeroom
    path('api/homeroom/gethomeappliance',views.gethomeappliances,name='gethomeappliance'),#to get data of homeappliances
    path('api/officeroom/getofficeroom',views.getOffice,name='getofficeroom'),#to get officeroom
    path('api/officeroom/getofficeappliance',views.getofficeappliances,name='getofficeappliance'),#toget officeappliance
    path('api/homeroom/deletehomeroom/<int:id>',views.deletehomeroom,name='deletehomeroom'),#toge
    path('api/homeroom/deletehomeappliance/<int:id>',views.deletehomeappliance,name='deletehomeappliance'),
    path('api/officeroom/deleteofficeroom/<int:id>',views.deleteofficeroom,name='deleteofficeroom'),
    path('api/officeroom/deleteofficeappliance/<int:id',views.deleteofficeappliance,name='deleteofficeappliance'),
    path('api/homeroom/update_home_room/<int:id>',views.update_home_room,name='update_home_room'),
    path('api/homeroom/update_home_appliance/<int:id>',views.update_home_appliance,name='update_home_appliance'),
    path('api/officeroom/update_office/<int:id>',views.update_office,name='update_office'),
    path('api/officeroom/update_officeappliance/<int:id>',views.update_officeappliance,name='update_officeappliance'),
    


   

]