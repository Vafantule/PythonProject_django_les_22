from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(forms.ModelForm):
    """
    Форма регистрации пользователя с email и паролем.
    """
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    Форма авторизации пользователя по email и паролю.
    """
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
