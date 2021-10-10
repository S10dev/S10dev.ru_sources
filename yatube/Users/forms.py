from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from Users.models import UserProfile
User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = {'avatar'}
