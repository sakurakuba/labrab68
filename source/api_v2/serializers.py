from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=2000, required=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    # test = serializers.CharField(max_length=30, write_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        return value

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, val in validated_data.items():
            setattr(instance, field, val)
        instance.save()
        return instance


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def validate_title(self, value):
        if len(value) < 3:
            raise ValidationError("Length too short")
        return value

