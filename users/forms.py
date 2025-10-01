from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    """
    Форма регистрации пользователя по email и паролю.
    """
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, label="Пароль")

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def save(self, commit: bool = True) -> CustomUser:
        """
        Создание пользователя и пароля.
        """
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
