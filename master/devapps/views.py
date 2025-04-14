# devapps/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from oauth2_provider.models import Application
from .forms import ApplicationRegistrationForm

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationRegistrationForm
    template_name = 'devapps/application_create.html'
    success_url = reverse_lazy('devapps:application_list')

    def form_valid(self, form):
        # Associe l'application au développeur (utilisateur connecté)
        form.instance.user = self.request.user
        print(f"User connected: {self.request.user}")
        return super().form_valid(form)

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'devapps/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Affiche uniquement les applications créées par l'utilisateur
        return Application.objects.filter(user=self.request.user)