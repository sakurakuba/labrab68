from django.db.models import Count
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from webapp.models import Article
from api_v2.serializers import ArticleModelSerializer


# Create your views here.
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    @action(methods=['GET'], detail=True, url_path="comments-count") # url path would be used as path
    def get_comments_count(self, request, *args, **kwargs):
        # return Response(self.queryset.aggregate(comments_count=Count("comments__id"))) # if detail=False
        return Response({"count": self.get_object().comments.count()}) # if detail=true

    # def get_serializer_class(self):
    #     pass

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny]
        return super().get_permissions()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({"status": "ok"})


