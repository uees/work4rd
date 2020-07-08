from rest_framework import viewsets, filters

from .models import MaterialCategory, Material
from .serializers import MaterialCategorySerializer, MaterialSerializer


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    queryset = MaterialCategory.objects.get_queryset()
    serializer_class = MaterialCategorySerializer
    search_fields = ('code', 'name', 'spec')


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.get_queryset()
    serializer_class = MaterialSerializer
    search_fields = ('code', 'name', 'spec')
    filter_fields = ('category', 'code')
