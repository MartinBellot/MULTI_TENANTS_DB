from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def home(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Connecte l'utilisateur
            return redirect('home')  # Redirige vers la page d'accueil ou une autre page
        else:
            print("Form is invalid")
    return render(request, 'home.html', {'form': form})