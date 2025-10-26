from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from delivery.models import DeliveryPerson, DeliveryZone

User = get_user_model()


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho hệ thống delivery'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample delivery data...\n')
        
        # Tạo nhân viên giao hàng
        self.create_delivery_persons()
        
        # Tạo khu vực giao hàng
        self.create_delivery_zones()
        
        self.stdout.write(self.style.SUCCESS('\nCompleted successfully!'))

    def create_delivery_persons(self):
        self.stdout.write('Creating delivery persons...')
        
        delivery_persons_data = [
            {
                'username': 'shipper1',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'shipper1@freshberry.com',
                'phone': '0901234567',
                'vehicle_type': 'motorbike',
                'vehicle_number': '59A-12345',
            },
            {
                'username': 'shipper2',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'shipper2@freshberry.com',
                'phone': '0902345678',
                'vehicle_type': 'motorbike',
                'vehicle_number': '59B-23456',
            },
            {
                'username': 'shipper3',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'email': 'shipper3@freshberry.com',
                'phone': '0903456789',
                'vehicle_type': 'car',
                'vehicle_number': '59C-34567',
            },
        ]
        
        for data in delivery_persons_data:
            # Tạo user nếu chưa tồn tại
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_staff': False,
                }
            )
            
            if created:
                user.set_password('shipper123')
                user.save()
                self.stdout.write(f'  + Created user: {user.username}')
            
            # Tạo DeliveryPerson nếu chưa tồn tại
            person, created = DeliveryPerson.objects.get_or_create(
                user=user,
                defaults={
                    'phone': data['phone'],
                    'vehicle_type': data['vehicle_type'],
                    'vehicle_number': data['vehicle_number'],
                    'is_active': True,
                    'rating': 5.0,
                }
            )
            
            if created:
                self.stdout.write(f'  + Created delivery person: {person}')

    def create_delivery_zones(self):
        self.stdout.write('\nCreating delivery zones...')
        
        zones_data = [
            {
                'name': 'Inner City HCMC',
                'base_fee': 20000,
                'additional_fee_per_km': 5000,
                'estimated_delivery_hours': 24,
                'districts': '''District 1
District 3
District 4
District 5
District 10
District 11
Phu Nhuan
Binh Thanh''',
            },
            {
                'name': 'Outer City HCMC',
                'base_fee': 30000,
                'additional_fee_per_km': 7000,
                'estimated_delivery_hours': 48,
                'districts': '''District 2
District 7
District 9
District 12
Thu Duc
Binh Tan
Tan Binh
Tan Phu''',
            },
            {
                'name': 'Nearby Provinces',
                'base_fee': 50000,
                'additional_fee_per_km': 10000,
                'estimated_delivery_hours': 72,
                'districts': '''Binh Duong
Dong Nai
Long An
Tay Ninh''',
            },
        ]
        
        for data in zones_data:
            zone, created = DeliveryZone.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            
            if created:
                self.stdout.write(f'  + Created zone: {zone.name}')
            else:
                self.stdout.write(f'  - Zone already exists: {zone.name}')

