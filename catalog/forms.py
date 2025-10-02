import re
from re import Pattern
from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS: tuple[str, ...] = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


def make_forbidden_pattern(text: str) -> Pattern[str | Any]:
    """
    Проверка исключаемых слов с учетом разделителей.
    """
    escaped = [re.escape(symbol) for symbol in text]
    pattern = r""
    for index, symbol in enumerate(escaped):
        pattern += symbol
        if index != len(escaped) -1:
            pattern += r"\W*"
    return re.compile(pattern, re.IGNORECASE | re.UNICODE)


FORBIDDEN_PATTERNS = [make_forbidden_pattern(word) for word in FORBIDDEN_WORDS]

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_FORMATS = ("image/jpeg", "image/png")

class ProductForm(forms.ModelForm):
    """
    Форма создания, редактирование продукта с проверкой на исключенные слова и проверка цены.
    """
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price", "status",]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Стилизация полей формы с помощью Bootstrap.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    def _check_forbidden(self, value: str, field_name: str) -> None:
        """
        Проверка исключаемых слов по поттерну.
        """
        for word, pattern in zip(FORBIDDEN_WORDS, FORBIDDEN_PATTERNS):
            if pattern.search(value):
                raise ValidationError(f"{field_name} не должно содержать слово: {word}")

    def clean_name(self) -> None:
        """
        Проверка исключенных слов в поле "name".
        """
        name = self.cleaned_data.get("name", "")
        self._check_forbidden(name, "Название")
        return name

    def clean_description(self) -> None:
        """
        Проверка исключенных слов в поле "description".
        """
        description = self.cleaned_data.get("description", "")
        self._check_forbidden(description, "Описание")
        return description

    def clean_price(self) -> None:
        """
        Проверка цены товара не отрицательна.
        """
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена товара не должна быть отрицательной.")
        return price

    def clean_image(self) -> Any:
        """
        Проверка формата и размера изображения.
        """
        image = self.cleaned_data.get("image")
        if image:
            if hasattr(image, "content_type"):
                if image.content_type not in ALLOWED_IMAGE_FORMATS:
                    raise ValidationError("Разрешены форматы изображений: JPEG, PNG")
            if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"Размер изображения не должен превышать {MAX_IMAGE_SIZE_MB} МБ")
        return image
