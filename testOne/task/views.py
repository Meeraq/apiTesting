from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .task import create_random_user_accounts

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def generate(request):
    total = 10
    create_random_user_accounts.delay(total)
    return Response({'details': 'success', 'data': {}}, status=201)
