from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.core.management import call_command


class Command(BaseCommand):
    """
    Кастомная команда для загрузки тестовых продуктов из фикстур.
    """
    help = "Загрузка продуктов и категорий из фикстур."

    def handle(self, *args, **options) -> None:
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("Удалены все продукты и категории..."))
        call_command("loaddata", "static/category.fixture.json")
        call_command("loaddata", "static/product.fixture.json")
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены."))
