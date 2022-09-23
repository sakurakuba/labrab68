from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Article
from webapp.models import Comment
from webapp.models import Tag


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


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "id")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class ArticleModelSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), many=True)
    # tags = TagSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = TagSerializer(instance.tags.all(), many=True).data
        return data



    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def validate_title(self, value):
        if len(value) < 3:
            raise ValidationError("Length too short")
        return value

