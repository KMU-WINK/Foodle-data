from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Menu
        fields = ['name']

class BannedMenuSerializer(serializers.Serializer):
    ban = serializers.ListField(help_text="싫어하는 메뉴")