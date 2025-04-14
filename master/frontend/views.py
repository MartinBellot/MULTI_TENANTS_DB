from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admin')
    return render(request, 'home.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin:index', {'message': "Super administrateur : fonctionnalité en cours de développement."})
    else:
        return render(request, 'admin:index', {'message': "Utilisateur : fonctionnalité en cours de développement."})