from django.views.generic import CreateView
import datetime as dt
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CreationForm, UserForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
User = get_user_model()


class SignUp(CreateView):
    """Signup class based view"""
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


def year(request):
    """Returns a current year in footer.html"""
    current_year = dt.datetime.now().year
    return {"current_year": current_year}
    

@login_required()
def upload_avatar(request, username):
    """Uploading an avatar to the profile"""
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('profile', username=username)
    if UserProfile.objects.filter(user=user).exists():
        userprofile = UserProfile.objects.get(user=user)
    else:
        userprofile = UserProfile.objects.create(user=user)
    form = UserForm(
        request.POST or None,
        files=request.FILES or None,
        instance=userprofile
        )
    if form.is_valid():
        form.save()
        return redirect('profile', username=username)
    return render(request, 'avatar.html', {'form': form})
