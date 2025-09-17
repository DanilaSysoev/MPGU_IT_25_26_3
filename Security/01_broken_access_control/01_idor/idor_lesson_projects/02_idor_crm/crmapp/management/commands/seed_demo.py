from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import *

class Command(BaseCommand):
    help = "Create demo users and sample objects"
    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(username='adminroot')
        if created:
            admin.set_password('adminroot123'); admin.is_superuser=True; admin.is_staff=True; admin.save()
        dev, created = User.objects.get_or_create(username='dev')
        if created:
            dev.set_password('devpass123'); dev.save()
        mod, created = User.objects.get_or_create(username='mod')
        if created:
            mod.set_password('modpass123'); mod.save()
        from ...models import Client
        if not Client.objects.exists():
            Client.objects.create(owner=dev, name='Dev Client A')
            Client.objects.create(owner=mod, name='Mod Client X')
        from ...models import Deal
        if not Deal.objects.exists():
            Deal.objects.create(owner=dev, title='Dev Deal A')
            Deal.objects.create(owner=mod, title='Mod Deal X')
        self.stdout.write(self.style.SUCCESS('Seeded users: adminroot/adminroot123, dev/devpass123, mod/modpass123'))
