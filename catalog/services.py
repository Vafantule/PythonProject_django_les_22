from typing import List
from .models import Product, Category


def get_products_by_category(category_id: int) -> List[Product]:
    """
    Возвращает список продуктов в указанной категории.
    """
    return Product.objects.filter(category_id=category_id)
