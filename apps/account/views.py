from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions  # noqa
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, GroupSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request: Request, format=None):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
