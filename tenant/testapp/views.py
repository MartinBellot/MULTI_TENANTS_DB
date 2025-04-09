from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from tenant.authentication import MasterIntrospectionAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([MasterIntrospectionAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': 'Accès autorisé via OAuth2 (introspection) !'})