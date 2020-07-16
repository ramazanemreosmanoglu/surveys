from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, forms
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

UserCreationForm = RegisterForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        url = request.GET.get("next")
        if url:
            return redirect(url)
        else:
            return redirect("/")

    return render(request, "accounts/form.html", {"form": form, 'title': 'Oturum Aç'})


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        messages.success(request, "")
        return redirect('home')

    return render(request, "accounts/form.html", {"form": form, 'title': 'Kaydol'})


def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def settings(request):
    #class SettingsForm(forms.Form):
     #   first_name = forms.CharField(label="İsim", required=False, value=request.user.first_name)
     #   last_name = forms.CharField(label="Soyisim", required=False, value=request.user.last_name)

    #form = SettingsForm(request.POST or None)

    form = request.POST
    if form:
        fname = form.get("first_name")
        lname = form.get("last_name")

        u = User.objects.get(username=request.user.username)

        u.first_name = fname

        u.last_name = lname
        u.save()
        messages.success(request, "Bilgileriniz Güncellendi.")

    context = dict(
        form=form
    )

    return render(request, "accounts/settings.html", context=context)


