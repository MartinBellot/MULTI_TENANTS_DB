from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser

def home(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'home.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        all_files = CustomUser.objects.all()
        return render(request, 'dashboard.html', {'all_files': all_files})
    else:
        user_files = CustomUser.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'user_files': user_files})