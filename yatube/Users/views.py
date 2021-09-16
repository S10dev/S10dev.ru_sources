#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView
import datetime as dt
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, UserForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"
    
def year(request):
    current_year = dt.datetime.now().year
    return {"current_year": current_year}
    
    
@login_required()
def get_avatar(request,username):
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('profile', username=username)
    if UserProfile.objects.filter(user = user).exists():
        usprof = UserProfile.objects.get(user = user)
    else:
        usprof = UserProfile.objects.create(user=user)
    form = UserForm(request.POST or None, files=request.FILES or None, instance=usprof)
    if form.is_valid():
        form.save()
        return redirect('profile', username=username)
    return render(request,'avatar.html',{'form':form})