"""
Management command to setup Shipper group and assign existing delivery persons
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from delivery.models import Delivery, DeliveryPerson


class Command(BaseCommand):
    help = 'Setup Shipper group with permissions and assign existing delivery persons'

    def handle(self, *args, **options):
        # Create Shipper group
        shipper_group, created = Group.objects.get_or_create(name='Shipper')
        
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Created "Shipper" group'))
        else:
            self.stdout.write(self.style.WARNING('[!] "Shipper" group already exists'))
        
        # Get content types
        delivery_ct = ContentType.objects.get_for_model(Delivery)
        
        # Define permissions for shippers
        permission_codenames = [
            'view_delivery',
            'change_delivery',  # They can update status
        ]
        
        # Add permissions to group
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(
                    content_type=delivery_ct,
                    codename=codename
                )
                shipper_group.permissions.add(permission)
                self.stdout.write(f'  [+] Added permission: {codename}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  [-] Permission not found: {codename}'))
        
        # Assign all DeliveryPerson users to Shipper group
        delivery_persons = DeliveryPerson.objects.select_related('user').all()
        assigned_count = 0
        
        for dp in delivery_persons:
            if dp.user:
                dp.user.groups.add(shipper_group)
                assigned_count += 1
                self.stdout.write(f'  [+] Assigned {dp.user.username} to Shipper group')
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Setup completed! {assigned_count} delivery persons assigned to Shipper group'))

