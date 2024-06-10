from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from userpanel.models import *
from userpanel.serializer import *
from rest_framework.authtoken.models import Token

# Endpoint for admin login
@api_view(['POST'])
def admin_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login success', 'username': username, 'email': user.email, 'token': token.key})
        else:
            return Response({'message': 'Invalid login details or not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get all rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_rooms_of_all(request):
    try:
        rooms = Home.objects.all()
        serializer = MyModelSerializer(rooms, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get all home appliances
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_homeappliance_of_all(request):
    try:
        homeappliances = HomeAppliance.objects.all()
        serializer = HomeApplianceserializer(homeappliances, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get all office rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officerooms_of_all(request):
    try:
        officerooms = Office.objects.all()
        serializer = Officeserializer(officerooms, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get all office appliances
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officeappliance_of_all(request):
    try:
        officeappliances = OfficeAppliance.objects.all()
        serializer = OfficeApplianceserializer(officeappliances, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get user details by ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def userdetails(request, id):
    try:
        details = []
        user = User.objects.filter(id=id).first()
        homeappliances = HomeAppliance.objects.filter(added_by=user.id)
        officeappliances = OfficeAppliance.objects.filter(added_by=user.id)

        for appliance in homeappliances:
            details.append({
                'id': appliance.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room': appliance.room.id  # Assuming you want the ID of the room
            })
        for appliance in officeappliances:
            details.append({
                'id': appliance.id,
                'addedby': appliance.added_by.id,
                'appliancename': appliance.name,
                'switchname': appliance.switchname,
                'room': appliance.officeroom.id  # Assuming you want the ID of the room
            })

        return Response(details)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get details of a room by ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_room_details_id(request, id):
    try:
        room = Home.objects.get(id=id)
        serializer = MyModelSerializer(room)
        return Response(serializer.data)
    except Home.DoesNotExist:
        return Response({"status": "failed", "error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get details of a home appliance by ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_homeappliance_details_id(request, id):
    try:
        homeappliance = HomeAppliance.objects.get(id=id)
        serializer = HomeApplianceserializer(homeappliance)
        return Response(serializer.data)
    except HomeAppliance.DoesNotExist:
        return Response({"status": "failed", "error": "Home appliance does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Endpoint to get all office rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officerooms_of_all(request):
    try:
        officerooms = Office.objects.all()
        serializer = Officeserializer(officerooms, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get all office appliances
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officeappliance_of_all(request):
    try:
        officeappliances = OfficeAppliance.objects.all()
        serializer = OfficeApplianceserializer(officeappliances, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get details of an office room by ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officeroom_details_id(request, id):
    try:
        officeroom = Office.objects.get(id=id)
        serializer = Officeserializer(officeroom)
        return Response(serializer.data)
    except Office.DoesNotExist:
        return Response({"status": "failed", "error": "Office room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint to get details of an office appliance by ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_officeappliance_details_id(request, id):
    try:
        officeappliance = OfficeAppliance.objects.get(id=id)
        serializer = OfficeApplianceserializer(officeappliance)
        return Response(serializer.data)
    except OfficeAppliance.DoesNotExist:
        return Response({"status": "failed", "error": "Office appliance does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# Endpoint to get total count of users and their details
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users_details(request):
    try:
        print("**********************")
        users = User.objects.all()
        total_count = users.count()

        user_details = []
        for user in users:
            home_appliances = HomeAppliance.objects.filter(added_by=user)
            office_appliances = OfficeAppliance.objects.filter(added_by=user)
            
            user_details.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'home_appliances': [
                    {
                        'id': appliance.id,
                        'name': appliance.name,
                        'switchname': appliance.switchname,
                        'room': appliance.room.id
                    }
                    for appliance in home_appliances
                ],
                'office_appliances': [
                    {
                        'id': appliance.id,
                        'name': appliance.name,
                        'switchname': appliance.switchname,
                        'officeroom': appliance.officeroom.id
                    }
                    for appliance in office_appliances
                ]
            })

        return Response({'total_count': total_count, 'users': user_details}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
