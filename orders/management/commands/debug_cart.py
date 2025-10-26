"""
Management command to debug cart sessions
"""
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'Debug all active cart sessions'

    def handle(self, *args, **options):
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        
        self.stdout.write(f"\nFound {active_sessions.count()} active sessions\n")
        
        for i, session in enumerate(active_sessions, 1):
            data = session.get_decoded()
            cart = data.get('cart', {})
            
            if cart:
                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"Session {i}: {session.session_key[:10]}...")
                self.stdout.write(f"Expires: {session.expire_date}")
                self.stdout.write(f"\nCart data:")
                self.stdout.write(json.dumps(cart, indent=2))
                
                # Calculate count
                count = 0
                for product_id, item in cart.items():
                    if isinstance(item, dict):
                        qty = item.get('quantity', 0)
                        count += qty
                        self.stdout.write(f"  Product {product_id}: {qty} items (dict format)")
                    else:
                        count += item
                        self.stdout.write(f"  Product {product_id}: {item} items (old format)")
                
                self.stdout.write(f"\nTotal count: {count}")
                self.stdout.write(f"{'='*60}\n")
        
        if not any(session.get_decoded().get('cart') for session in active_sessions):
            self.stdout.write(self.style.WARNING("No carts found in any session"))

