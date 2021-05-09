from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)
