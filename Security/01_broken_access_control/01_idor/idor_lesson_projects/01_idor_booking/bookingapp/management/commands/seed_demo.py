from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import *

class Command(BaseCommand):
    help = "Create demo users and sample objects"
    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(username='adminroot')
        if not admin.has_usable_password():
            admin.set_password('adminroot123'); admin.is_superuser=True; admin.is_staff=True; admin.save()
        dev, _ = User.objects.get_or_create(username='dev')
        if not dev.has_usable_password():
            dev.set_password('devpass123'); dev.save()
        mod, _ = User.objects.get_or_create(username='mod')
        if not mod.has_usable_password():
            mod.set_password('modpass123'); mod.save()
        from ...models import Booking
        if not Booking.objects.exists():
            Booking.objects.create(owner=dev, title='Dev Booking A')
            Booking.objects.create(owner=mod, title='Mod Booking X')
        from ...models import Payment
        if not Payment.objects.exists():
            Payment.objects.create(owner=dev, title='Dev Payment A')
            Payment.objects.create(owner=mod, title='Mod Payment X')
        self.stdout.write(self.style.SUCCESS('Seeded users: adminroot/adminroot123, dev/devpass123, mod/modpass123'))
