from django.contrib.auth.models import User
from django.test import TestCase
from .models import Home, HomeAppliance, Office, OfficeAppliance
from .serializer import MyModelSerializer, HomeApplianceserializer, Officeserializer, OfficeApplianceserializer, UserSerializer

class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.home = Home.objects.create(room='Living Room', added_by=self.user)
        self.home_appliance = HomeAppliance.objects.create(name='Television', switchname='TV Switch', room=self.home, added_by=self.user)
        self.office = Office.objects.create(officeroom='Office Room 1', added_by=self.user)
        self.office_appliance = OfficeAppliance.objects.create(name='Laptop', switchname='Laptop Switch', officeroom=self.office, added_by=self.user)
        
    def test_mymodel_serializer(self):
        serializer = MyModelSerializer(instance=self.home)
        self.assertEqual(serializer.data['room'], 'Living Room')
        self.assertEqual(serializer.data['added_by'], self.user.id)

    def test_home_appliance_serializer(self):
        serializer = HomeApplianceserializer(instance=self.home_appliance)
        self.assertEqual(serializer.data['name'], 'Television')
        self.assertEqual(serializer.data['switchname'], 'TV Switch')
        self.assertEqual(serializer.data['room'], self.home.id)
        self.assertEqual(serializer.data['added_by'], self.user.id)

    def test_office_serializer(self):
        serializer = Officeserializer(instance=self.office)
        self.assertEqual(serializer.data['officeroom'], 'Office Room 1')
        self.assertEqual(serializer.data['added_by'], self.user.id)

    def test_office_appliance_serializer(self):
        serializer = OfficeApplianceserializer(instance=self.office_appliance)
        self.assertEqual(serializer.data['name'], 'Laptop')
        self.assertEqual(serializer.data['switchname'], 'Laptop Switch')
        self.assertEqual(serializer.data['officeroom'], self.office.id)
        self.assertEqual(serializer.data['added_by'], self.user.id)

    def test_user_serializer(self):
        serializer_data = {'username': 'testuser2', 'email': 'test2@example.com', 'password': 'testpassword2'}
        serializer = UserSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, serializer_data['username'])
        self.assertEqual(user.email, serializer_data['email'])
