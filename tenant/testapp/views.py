from django.http import JsonResponse
from oauth2_provider.decorators import protected_resource

@protected_resource()
def test_view(request):
    """
    Vue de test accessible uniquement si le token OAuth est valide.
    """
    return JsonResponse({'message': 'Accès autorisé via OAuth depuis Master'})