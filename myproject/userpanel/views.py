from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import HomeAppliance
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
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import Home, Office, HomeAppliance, OfficeAppliance
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import HomeAppliance, OfficeAppliance
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import HomeAppliance, OfficeAppliance
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import HomeApplianceStatus
from .serializer import HomeApplianceStatusSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from userpanel.mqtt import MQTTHandler
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import HomeAppliance, OfficeAppliance, HomeApplianceStatus, OfficeApplianceStatus
from .mqtt import mqtt_handler
import logging

def is_admin(user):
    return user.is_authenticated and user.is_staff


#for adding rooms in home
from rest_framework.exceptions import ParseError


    
from rest_framework.response import Response



@api_view(['POST'])
def user_register(request):
    try:
        data = request.data
        email = data['email']
        password = data['password']
        # username = data['username']

        
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
def user_login(request):
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
        return Response({'message': 'Login successful','Token':token.key,'email':email,'id':id,'username':username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
from django.contrib.auth import logout
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response('user logout')



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





from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Home
from .serializer import HomeApplianceserializer

@api_view(['POST'])
def add_homeappliances(request, room_id):
    try:
        user = request.user

        # Retrieve the room object from the database using the room_id
        room = get_object_or_404(Home, id=room_id)

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


#for adding rooms in office
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def add_officeroom(request):
    try:
        # Extract the user from the request (assuming you're using TokenAuthentication or similar)
        user = request.user
        id = user.id
        print(id)
        # print('user', user)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the user to the mutable data
        mutable_data['added_by'] = id

        # Create the serializer with modified data
        serializer = Officeserializer(data=mutable_data)

        # Validate and save the serializer
        if serializer.is_valid():
            instance = serializer.save()
            
            # Customize the response data
            response_data = {
                'room': instance.officeroom,
                'id': instance.id,
                'data': serializer.data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Office, OfficeAppliance
from .serializer import Officeserializer, OfficeApplianceserializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_officeappliances(request, officeroom_id):
    try:
        # Extract the user from the request (assuming you're using TokenAuthentication or similar)
        user = request.user

        # Retrieve the room object from the database using officeroom_id
        room = get_object_or_404(Office, id=officeroom_id)

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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gethomeappliances(request):
    try:
        user = request.user
        q = HomeAppliance.objects.filter(added_by=user)
        appliance_data = []
        
        for appliance in q:
            appliance_data.append({
                'id': appliance.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room_id': appliance.room.id
            })

        response_data = {
            'success': True,
            'message': 'Home appliances retrieved successfully.',
            'data': appliance_data
        }

        return Response(response_data)
    except Exception as e:
        error_response = {
            'success': False,
            'message': str(e)
        }
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getofficeappliances(request):
    try:
        user = request.user
        q = OfficeAppliance.objects.filter(added_by=user)
        appliance_data = []
        
        for appliance in q:
            appliance_data.append({
                'id': appliance.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room_id': appliance.officeroom.id
            })

        response_data = {
            'success': True,
            'message': 'Office appliances retrieved successfully.',
            'data': appliance_data
        }

        return Response(response_data)
    except Exception as e:
        error_response = {
            'success': False,
            'message': str(e)
        }
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Home, Office
from django.http import Http404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_room_by_id(request, room_id):
    try:
        # Check if the room exists for the authenticated user using added_by_id and mongodb_id
        rooms = Home.objects.filter(added_by_id=room_id, added_by=request.user)
        
        # Print the rooms queryset for debugging purposes
        print(f"Rooms: {rooms}")
        
        if not rooms.exists():
            raise Home.DoesNotExist
        
        # Format the room details for the response
        room_details = []
        for room in rooms:
            room_details.append({
                'room_id': room.id,
                'room_name': room.room,
                'added_by': room.added_by.username if room.added_by else None
            })
        
        # Return the rooms details for debugging
        return Response({'room_details': room_details, 'rooms': str(rooms)}, status=status.HTTP_200_OK)
        
    except Home.DoesNotExist:
        raise Http404("Room doesn't exist or you don't have permission to access it")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_office_room_by_id(request, room_id):
    try:
        # Check if the room exists for the authenticated user using added_by_id and mongodb_id
        rooms = Office.objects.filter(added_by_id=room_id, added_by=request.user)
        
        # Print the rooms queryset for debugging purposes
        print(f"Rooms: {rooms}")
        
        if not rooms.exists():
            raise Home.DoesNotExist
        
        # Format the room details for the response
        room_details = []
        for room in rooms:
            room_details.append({
                'room_id': room.id,
                'office_room_name': room.officeroom,
                'added_by': room.added_by.username if room.added_by else None
            })
        
        # Return the rooms details for debugging
        return Response({'room_details': room_details, 'rooms': str(rooms)}, status=status.HTTP_200_OK)
        
    except Home.DoesNotExist:
        raise Http404("Room doesn't exist or you don't have permission to access it")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appliance_details_by_room_id(request, room_id):
    try:
        # Check if the room ID exists for the authenticated user
        if not Home.objects.filter(added_by=request.user, id=room_id).exists():
            raise Http404("Room ID doesn't exist")

        appliances = HomeAppliance.objects.filter(room=room_id, added_by=request.user)
        appliance_data = []

        for appliance in appliances:
            appliance_data.append({
                'id': appliance.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room_id': appliance.room.id
            })

        response_data = {
            'success': True,
            'message': 'Appliances retrieved successfully.',
            'data': appliance_data
        }

        return Response(response_data)
    except Http404 as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_office_details_by_office_id(request, room_id):
    try:
        office = Office.objects.get(id=room_id, added_by=request.user)
        print(office.id, "**************")
        appliances = OfficeAppliance.objects.filter(officeroom_id=room_id, added_by=request.user)
        office_details = {
            'office_id': office.id,
            'office_name': office.officeroom,
            'added_by': office.added_by.username if office.added_by else None,
            'appliances': []
        }
        
        if not appliances:
            return Response({'error': f"No appliances found for office with ID {room_id} or you don't have access to them"}, status=status.HTTP_404_NOT_FOUND)
        
        for appliance in appliances:
            appliance_data = {
                'appliance_id': appliance.id,
                'appliance_name': appliance.name,
                'switch_name': appliance.switchname,
                'added_by': appliance.added_by.username if appliance.added_by else None
            }
            office_details['appliances'].append(appliance_data)   
        
        username = request.user.username
        
        return Response({'username': username, 'office_details': office_details}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#deleting homerooms
    

@api_view(['DELETE'])

def delete_homeroom(request,id):
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

def delete_home_appliance(request,id):
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

def delete_office_room(request,id):
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
@permission_classes([IsAuthenticated])
def delete_office_appliance(request, id):
    try:
        # Find the office appliance by ID
        office_appliance = get_object_or_404(OfficeAppliance, id=id)
        
        # Delete the office appliance
        office_appliance.delete()
        
        return Response({"message": "Office appliance deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

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
@permission_classes([IsAuthenticated])
def update_home_appliance(request, id):
    try:
        # Retrieve the home appliance from the database
        home_appliance = get_object_or_404(HomeAppliance, id=id)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Handle 'room' if it's provided in the request data
        if 'room' in mutable_data:
            room_id = mutable_data.pop('room')
            room = get_object_or_404(Home, id=room_id)
            mutable_data['room'] = room.id

        # Update the home appliance with the new data from the request
        serializer = HomeApplianceserializer(instance=home_appliance, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


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
        user = request.user
        # Retrieve the office appliance from the database
        office_appliance = get_object_or_404(OfficeAppliance, id=id)

        # Make a copy of the request data to modify
        mutable_data = request.data.copy()

        # Remove 'officeroom' field if present
        mutable_data.pop('officeroom', None)

        # Add the user to the mutable data
        mutable_data['added_by'] = user.id

        # Update the office appliance with the new data
        serializer = OfficeApplianceserializer(instance=office_appliance, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response(str(e), status=500)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_rooms_by_user(request, user_id):
    try:
        # Retrieve all home and office rooms associated with the user
        home_rooms = Home.objects.filter(added_by=user_id)
        office_rooms = Office.objects.filter(added_by=user_id)

        # Serialize home rooms
        home_rooms_data = []
        for room in home_rooms:
            home_rooms_data.append({
                'room_id': room.id,
                'room_name': room.room,
                'type': 'home'
            })

        # Serialize office rooms
        office_rooms_data = []
        for room in office_rooms:
            office_rooms_data.append({
                'id': room.id,
                'office_room_name': room.officeroom,
                'type': 'office'
            })

        # Combine home and office room data
        all_rooms_data = {
            'home_rooms': home_rooms_data,
            'office_rooms': office_rooms_data
        }

        return Response(all_rooms_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

mqtt_handler = MQTTHandler()


logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def receive_status(request, user_id):
    try:
        # Query database to retrieve appliances based on user ID
        home_appliances = HomeAppliance.objects.filter(added_by=user_id)
        office_appliances = OfficeAppliance.objects.filter(added_by=user_id)
        
        # Construct and send MQTT messages for each appliance
        for appliance in home_appliances:
            message = f"Home, {appliance.switchname}, {appliance.name}, {appliance.room}"
            topic = 'mqtt/home/devicestatus'
            mqtt_handler.publish(topic, message)
        
        for appliance in office_appliances:
            message = f"Office, {appliance.switchname}, {appliance.name}, {appliance.officeroom}"
            topic = 'mqtt/office/devicestatus'
            mqtt_handler.publish(topic, message)
        
        # Subscribe to topics to receive acknowledgment or updates
        received_messages = {}
        for topic in ['mqtt/home/devicestatus', 'mqtt/office/devicestatus']:
            received_message = mqtt_handler.subscribe_with_timeout(topic, timeout=10)
            received_messages[topic] = received_message

        # Retrieve additional details and format the response
        response_data = []
        for appliance in home_appliances:
            room_name = appliance.room.room
            status = received_messages.get(f'mqtt/home/devicestatus', {}).get('status')
            response_data.append({
                "username": request.user.username,
                "user_id": request.user.id,
                "appliance_name": appliance.name,
                "appliance_id": appliance.id,
                "room_name": room_name,
                "room_id": appliance.room.id,
                "status": status
            })

        for appliance in office_appliances:
            room_name = appliance.officeroom.officeroom
            status = received_messages.get(f'mqtt/office/devicestatus', {}).get('status')
            response_data.append({
                "username": request.user.username,
                "user_id": request.user.id,
                "appliance_name": appliance.name,
                "appliance_id": appliance.id,
                "room_name": room_name,
                "room_id": appliance.officeroom.id,
                "status": status
            })

        return JsonResponse({'received_messages': response_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_home_appliance_status(request, home_id, appliance_id):
    if request.method == 'POST':
        # Define the MQTT topic based on the home_id and appliance_id
        topic = f"home/{home_id}/appliances/{appliance_id}/status"

        # Assuming the status is passed in the request data
        status = request.data.get('status', '').strip().lower()

        if status not in ["on", "off"]:
            return Response({"error": "Invalid status. Status must be 'on' or 'off'."}, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            home_appliance = HomeAppliance.objects.get(id=appliance_id, room_id=home_id)
        except HomeAppliance.DoesNotExist:
            return Response({"error": "Home appliance not found."}, status=http_status.HTTP_404_NOT_FOUND)

        home_appliance_status, created = HomeApplianceStatus.objects.get_or_create(appliance=home_appliance)
        home_appliance_status.status = (status == "on")
        home_appliance_status.save()

        # Publish the status update to MQTT topic
        mqtt_handler.publish(topic, status)

        # Include device_name, room_name, and username in the response
        device_name = home_appliance.name
        room_name = home_appliance.room.room
        username = request.user.username
        user_id = request.user.id

        return Response({
            "username": username,
            "user_id": user_id,
            "appliance_name": device_name,
            "appliance_id": appliance_id,
            "room_name": room_name,
            "room_id": home_appliance.room.id,
            "status": status
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_home_appliance_status(request, status_id):
    try:
        # Retrieve the HomeApplianceStatus object based on the provided status ID
        status = get_object_or_404(HomeApplianceStatus, id=status_id)

        # Serialize the status object
        serializer = HomeApplianceStatusSerializer(status)
        
        # Include additional information in the response
        home_appliance = status.appliance
        room_name = home_appliance.room.room
        device_name = home_appliance.name
        username = request.user.username

        response_data = serializer.data
        response_data.update({
            "username": username,
            "appliance_name": device_name,
            "room_name": room_name
        })

        return Response(response_data, status=http_status.HTTP_200_OK)
    except HomeApplianceStatus.DoesNotExist:
        return Response({"error": "Home appliance status not found."}, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_home_appliance_status(request, status_id):
    try:
        user = request.user
        status = get_object_or_404(HomeApplianceStatus, id=status_id, added_by=user)
        status.delete()
        return Response("Home appliance status deleted successfully", status=http_status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(str(e), status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_office_appliance_status(request, office_id, appliance_id):
    if request.method == 'POST':
        # Define the MQTT topic based on the office_id and appliance_id
        topic = f"office/{office_id}/appliances/{appliance_id}/status"

        # Assuming the status is passed in the request data
        status = request.data.get('status', '').strip().lower()

        if status not in ["on", "off"]:
            return Response({"error": "Invalid status. Status must be 'on' or 'off'."}, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            office_appliance = OfficeAppliance.objects.get(id=appliance_id, officeroom_id=office_id)
        except OfficeAppliance.DoesNotExist:
            return Response({"error": "Office appliance not found."}, status=http_status.HTTP_404_NOT_FOUND)

        # Create or update the OfficeApplianceStatus
        office_appliance_status, created = OfficeApplianceStatus.objects.get_or_create(appliance=office_appliance)
        office_appliance_status.status = (status == "on")
        office_appliance_status.save()

        # Publish the status update to MQTT topic
        mqtt_handler.publish(topic, status)

        # Include device_name, room_name, and username in the response
        device_name = office_appliance.name
        room_name = office_appliance.officeroom.officeroom
        username = request.user.username

        return Response({
            "username": username,
            "appliance_name": device_name,
            "room_name": room_name,
            "status": status
        }, status=http_status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_office_appliance_status(request, status_id):
    try:
        user = request.user
        status = get_object_or_404(OfficeApplianceStatus, id=status_id, added_by=user)
        status.delete()
        return Response("Office appliance status deleted successfully", status=http_status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(str(e), status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_office_appliance_status(request, status_id):
    try:
        # Retrieve the OfficeApplianceStatus object based on the provided status ID
        status = get_object_or_404(OfficeApplianceStatus, id=status_id)

        # Serialize the status object
        serializer = OfficeApplianceStatusSerializer(status)
        
        # Include additional information in the response
        office_appliance = status.appliance
        room_name = office_appliance.officeroom.officeroom
        device_name = office_appliance.name
        username = request.user.username

        response_data = serializer.data
        response_data.update({
            "username": username,
            "appliance_name": device_name,
            "room_name": room_name
        })

        return Response(response_data, status=http_status.HTTP_200_OK)
    except OfficeApplianceStatus.DoesNotExist:
        return Response({"error": "Office appliance status not found."}, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
