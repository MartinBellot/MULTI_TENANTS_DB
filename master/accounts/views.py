from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

def home(request):
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

# Create your views here.
