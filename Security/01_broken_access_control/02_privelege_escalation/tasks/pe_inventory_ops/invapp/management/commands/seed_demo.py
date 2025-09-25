from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Profile, Item

class Command(BaseCommand):
    help = "Create demo users, profiles, items"
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

        Profile.objects.get_or_create(user=admin, defaults={'role':'admin'})
        Profile.objects.get_or_create(user=dev, defaults={'role':'user'})
        Profile.objects.get_or_create(user=mod, defaults={'role':'moderator'})

        if not Item.objects.exists():
            Item.objects.create(owner=admin, title="Админский документ")
            Item.objects.create(owner=dev, title="Заметка dev #1")
            Item.objects.create(owner=mod, title="Модераторская запись")
        self.stdout.write(self.style.SUCCESS("Seeded users: adminroot/adminroot123, dev/devpass123, mod/modpass123"))
