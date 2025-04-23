from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import string

def contains_special_character(value):
    return any(ch in string.punctuation for ch in value)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError("Passwords don’t match.")
        if len(pw1) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if not any(c.isupper() for c in pw1):
            raise ValidationError("Password must include an uppercase letter.")
        if not any(c.isdigit() for c in pw1):
            raise ValidationError("Password must include a digit.")
        if not contains_special_character(pw1):
            raise ValidationError("Password must include a special character.")
        return pw2

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = (
      "username",
      "email",
      "age",
      )