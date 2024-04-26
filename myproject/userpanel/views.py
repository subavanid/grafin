#adminpanel code

from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# # your_app/views.py

from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from django.http import JsonResponse








import time
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
import paho.mqtt.client as mqtt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404

from django.db.models import Count




# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authtoken.models import Token

def is_admin(user):
    return user.is_authenticated and user.is_staff


#for adding rooms in home
from rest_framework.exceptions import ParseError


# @authentication_classes([TokenAuthentication])
# # @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def add_room(request):
#     try:
#         # Extract the user from the request (assuming you're using TokenAuthentication or similar)
#         user = request.user
#         id=user.id
#         print(id)
#         print('user',user)

#         # Create a mutable copy of the request data
#         mutable_data = request.data.copy()

#         # Add the user to the mutable data
#         mutable_data['added_by'] = id
        

#         # Create the serializer with modified data
#         serializer = MyModelSerializer(data=mutable_data)

#         # Validate and save the serializer
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
from rest_framework.response import Response

@authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_room(request):
    try:
        # Extract the user from the request (assuming you're using TokenAuthentication or similar)
        user = request.user
        id = user.id
        print(id)
        print('user', user)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the user to the mutable data
        mutable_data['added_by'] = id

        # Create the serializer with modified data
        serializer = MyModelSerializer(data=mutable_data)

        # Validate and save the serializer
        if serializer.is_valid():
            instance = serializer.save()
            
            # Customize the response data
            response_data = {
                'room': instance.room,
                'id': instance.id,
                'data': serializer.data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#for adding appliances to home
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
@api_view(['POST'])

def add_homeappliances(request):
    try:
        # Extract the room name from the request data
        room_name = request.data.get('room')
        user = request.user

        # Check if the room name is provided
        if not room_name:
            return Response({'error': 'Room name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the room object from the database
        room = Home.objects.filter(room=room_name).first()

        # Check if the room exists
        if not room:
            return Response({'error': f"Room '{room_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the room object to the mutable data
        mutable_data['room'] = room.id
        mutable_data['added_by'] = user.id

        # Create the serializer with modified data
        serializer = HomeApplianceserializer(data=mutable_data)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#for adding rooms in office

# #for adding rooms in office

@api_view(['POST'])

def add_officeroom(request):
    try:
       
        # Extract the user from the request (assuming you're using TokenAuthentication or similar)
        user = request.user

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the user to the mutable data
        mutable_data['added_by'] = user.id

        # Create the serializer with modified data
        serializer = Officeserializer(data=mutable_data)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#for adding appliances to office
@api_view(['POST'])

def add_officeappliances(request):
    try:
        # Extract the room name from the request data
        room_name = request.data.get('room')
        user = request.user
        print(room_name)

        # Check if the room name is provided
        if not room_name:
            return Response({'error': 'Room name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the room object from the database
        room = Office.objects.filter(officeroom=room_name).first()
        print(room)

        # Check if the room exists
        if not room:
            return Response({'error': f"Room '{room_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the room object to the mutable data
        mutable_data['officeroom'] = room.id
        mutable_data['added_by'] = user.id

        # Create the serializer with modified data
        serializer = OfficeApplianceserializer(data=mutable_data)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#for getting homerooms


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_homeroom(request):
    try:
        # Get the current admin user
        user = request.user

        # Filter the queryset to get the data added by the admin user
        q = Home.objects.all()  # Retrieve a single instance
        
        room_data = []
        
        # Iterate through queryset to access attributes of individual appliances
        for room in q:
            room_data.append({
                'id': room.id,
                'addedby': user.id,
                'roomname': room.room,
                  # Assuming you want the ID of the room
            })

        return Response(room_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#for gettinghome appliances

    
@api_view(['GET'])
def gethomeappliances(request):
    try:
        user = request.user
        q = HomeAppliance.objects.all()
        print(q)
        appliance_data = []
        
        # Iterate through queryset to access attributes of individual appliances
        for appliance in q:
            appliance_data.append({
                'id': appliance.id,
                'addedby': appliance.added_by.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room': appliance.room.id  # Assuming you want the ID of the room
            })

        return Response(appliance_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])

def getOffice(request):
      try:
        # Get the current admin user
        user = request.user

        # Filter the queryset to get the data added by the admin user
        q = Office.objects.all()  # Retrieve a single instance
        # s=q['officeroom']
        if q:
             room_data = []
        
        # Iterate through queryset to access attributes of individual appliances
        for room in q:
            room_data.append({
                'id': room.id,
                'addedby': user.id,
                'roomname': room.officeroom,
                  # Assuming you want the ID of the room
            })

        return Response(room_data)
      except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#for gettinghome appliances
@api_view(['GET'])

def getofficeappliances(request):
    try:
        admin_user=request.user
        q = OfficeAppliance.objects.all()
        appliance_data = []
        
        # Iterate through queryset to access attributes of individual appliances
        for appliance in q:
            appliance_data.append({
                'id': appliance.id,
                'addedby': appliance.added_by.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room': appliance.officeroom.id  # Assuming you want the ID of the room
            })

        return Response(appliance_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Home
# from .serializer import HomeSerializer
from rest_framework import status

@api_view(['GET'])
def get_room_details(request):
    try:
        # Get the total count of rooms
        total_rooms = Home.objects.count()

        # Get room names along with details of associated appliances
        rooms_with_appliances = Home.objects.annotate(appliance_count=Count('homeappliance')).values(
            'room', 'appliance_count'
        )

        # Create response data
        response_data = {
            'total_rooms': total_rooms,
            'rooms_with_appliances': list(rooms_with_appliances)
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#deleting homerooms
    

@api_view(['DELETE'])

def deletehomeroom(request,id):
    try:
        # Find the home room by ID
        home_room = get_object_or_404(Home, id=id)
        
        # Delete the home room
        home_room.delete()
        
        return Response("Home room deleted successfully", status=204)
    except Exception as e:
        return Response(str(e), status=500)
    


#deleting home appliance
    

@api_view(['DELETE'])

def deletehomeappliance(request,id):
    try:
        # Find the home room by ID
        home_appliance = get_object_or_404(HomeAppliance, id=id)
        
        # Delete the home room
        home_appliance.delete()
        
        return Response("Home room deleted successfully", status=204)
    except Exception as e:
        return Response(str(e), status=500)
    

#deleting office room
    

@api_view(['DELETE'])

def deleteofficeroom(request,id):
    try:
        # Find the home room by ID
        office = get_object_or_404(Office, id=id)
        
        # Delete the home room
        office.delete()
        
        return Response("Home room deleted successfully", status=204)
    except Exception as e:
        return Response(str(e), status=500)
    



#deleting office appliance
    

@api_view(['DELETE'])

def deleteofficeappliance(request,id):
    try:
        # Find the home room by ID
        officeappliance = get_object_or_404(OfficeAppliance, id=id)
        
        # Delete the home room
        officeappliance.delete()
        
        return Response("Home room deleted successfully", status=204)
    except Exception as e:
        return Response(str(e), status=500)
    

#updating home room
@api_view(['PUT'])
def update_home_room(request, id):
    try:
        user=request.user
        # Retrieve the home room from the database
        home_room = get_object_or_404(Home, id=id)
        mutabledata=request.data.copy()
        mutabledata['added_by'] = user.id
        
        # Update the home room with the new data from the request
        serializer = MyModelSerializer(instance=home_room, data=mutabledata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response(str(e), status=500)
    

#updating homeappliance

@api_view(['PUT'])
def update_home_appliance(request, id):
    try:
        user = request.user
        # Retrieve the home appliance from the database
        home_appliance = get_object_or_404(HomeAppliance, id=id)
        room = Home.objects.get(room=request.data['room'])
       
        
        # Create a mutable copy of the request data
        mutable_data = request.data.copy()
        room_id = mutable_data.pop('room')  # Remove 'room' from mutable_data
        mutable_data['room'] = room.id 
        
        # Add the user to the mutable data
        mutable_data['added_by'] = user.id
        
        # Update the home appliance with the new data from the request
        serializer = HomeApplianceserializer(instance=home_appliance, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response(str(e), status=500)
    


#updating office

@api_view(['PUT'])
def update_office(request, id):
    try:
        user=request.user
        # Retrieve the home room from the database
        office_room = get_object_or_404(Office, id=id)
        mutabledata=request.data.copy()
        mutabledata['added_by']=user.id
        
        # Update the home room with the new data from the request
        serializer = Officeserializer(instance=office_room, data=mutabledata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response(str(e), status=500)  


#updating officeappliance

@api_view(['PUT'])
def update_officeappliance(request, id):
    try:
        # Retrieve the office appliance from the database
        office_appliance = get_object_or_404(OfficeAppliance, id=id)
        
        # Retrieve the office room from the database based on the provided name
        room_name = request.data.get('officeroom')
        room = Office.objects.get(officeroom=room_name)
        print(room)
        
        # Retrieve the current user
        user = request.user

        # Make a copy of the request data to modify
        mutable_data = request.data.copy()
        
        # Update the 'officeroom' field with the primary key of the office room
        mutable_data['officeroom'] = room.id
        
        # Add the user to the mutable data
        mutable_data['added_by'] = user.id
        
        # Update the office appliance with the new data
        serializer = OfficeApplianceserializer(instance=office_appliance, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response(str(e), status=500)


@api_view(['POST'])
def admin_register(request):
    try:
        data = request.data
        email = data['email']
        password = data['password']
        
        mutdata = data.copy()
        mutdata['is_superuser'] = False
        
        serializer = UserSerializer(data=mutdata)
        
        if serializer.is_valid():
            # Extract user data
            serializer.save()
            
            # Return a success response
            return Response('User Registered Successfully', status=201)  # Use status code 201 for successful creation
        else:
            # Return a validation error response
            return Response(serializer.errors, status=400)

    except Exception as e:
        # Return an error response
        return Response(str(e), status=500)
        



@api_view(['POST'])
def admin_login(request):
    data = request.data

    if 'email' not in data or 'password' not in data:
        return Response("Username and password required", status=status.HTTP_400_BAD_REQUEST)
    
    email = data['email']
    password = data['password']
    print(email,password)
    
    # Authenticate the user
    user = User.objects.filter(email=email).first()
    print(user)

    if user is not None:
        # Check if the user already has a token
        token, created = Token.objects.get_or_create(user=user)
        id=user.id
        username=user.username
        password=user.password
        
        # Return token as part of the response
        return Response({'message': 'Login successful','Token':token.key,'email':email,'password':password,'id':id,'username':username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
from django.contrib.auth import logout
@api_view(['POST'])
def admin_logout(request):
    logout(request)
    return Response('user logout')

















