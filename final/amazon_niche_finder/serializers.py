from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "cat_name", "cat_level", "cat_bestsellers_link")
