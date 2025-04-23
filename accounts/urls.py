from django.urls import path
from .forms import CustomUserCreationForm
from .views import SignUpView

urlpatterns = [
    path(
      "signup/", 
      SignUpView.as_view(form_class=CustomUserCreationForm), 
      name="signup"
    ),
]