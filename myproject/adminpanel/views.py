from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
# from .serializer import *
from userpanel.models import *
from userpanel.serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])

def admin_login(request):
    try:
        email=request.data.get('email')
        password=request.data.get('password')
        q=User.objects.filter(email=email).first()
        if q:
            return Response({'message':'Login sucess','email':email,'username':q.username})
        else:
            return Response({'message':'not successful'})
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    


@api_view(['GET'])
def get_rooms(request):
    try:
        q=Home.objects.all()
        serializer=MyModelSerializer(q,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
def get_homeappliance(request):
    try:
        q=HomeAppliance.objects.all()
        serializer=HomeApplianceserializer(q,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
def get_officerooms(request):
    try:
        q=Office.objects.all()
        serializer=Officeserializer(q,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
def get_officeappliance(request):
    try:
        q=OfficeAppliance.objects.all()
        serializer=OfficeApplianceserializer(q,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])

def userdetails(request,id):
    try:
        details=[]
        id=id
        user=User.objects.filter(id=id).first()
        homeappliance=HomeAppliance.objects.filter(added_by=user.id)
        officeappliance=OfficeAppliance.objects.filter(added_by=user.id)

        for appliance in homeappliance:
            details.append({
            
                    'id': appliance.id,
                    
                    'appliancename': appliance.name,
                    'switchname': appliance.switchname,
                    'room': appliance.room.id  # Assuming you want the ID of the room
                })
        for appliance in officeappliance:
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

    

        



