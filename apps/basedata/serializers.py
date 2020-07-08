from rest_framework import serializers

from .models import MaterialCategory, Material


class MaterialCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialCategory
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'
