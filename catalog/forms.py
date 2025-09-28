from typing import Any

from django import forms

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


class ProductForm(forms.ModelForm):
    """
    Форма создания, редактирование продукта с проверкой на исключенные слова и проверка цены.
    """
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price",]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Стилизация полей формы с помощью Bootstrap.
        """
        super().__init__(*args, **kwargs)
        for name, field in self.fields.item():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    def clean_name(self) -> None:
        """
        Проверка исключенных слов в поле "name".
        """
        name = self.cleaned_data.get("name", "")
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название не должно содержать слово: '{word}'")
        return name

    def clean_description(self) -> None:
        """
        Проверка исключенных слов в поле "description".
        """
        description = self.cleaned_data.get("description", "")
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Описание не должно содержать слово: '{word}'")
            return description
