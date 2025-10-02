from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' с необходимыми правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        can_unpublish = Permission.objects.get(
            codename="can_unpublish_product",
            content_type__app_label="catalog",
            content_tpe__model="product"
        )
        can_delete = Permission.objects.get(
            codename="can_delete_product",
            content_type__app_label="catalog",
            content_tpe__model="product"
        )
        group.permissions.set([can_unpublish, can_delete])
        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' обновлена"))
