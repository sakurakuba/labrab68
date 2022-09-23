import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from webapp.models import Article
from api_v2.serializers import ArticleSerializer


# Create your views here.


class ArticleView(View):
    serializer_class = ArticleSerializer
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        # print(articles)
        # print(self.serializer_class(articles, many=True).data)  # if sending list objects need add many=True
        articles_data = self.serializer_class(articles, many=True).data
        return JsonResponse(articles_data, safe=False)

    def post(self, request, *args, **kwargs):
        if request.body:
            body = json.loads(request.body)
            serializer = self.serializer_class(data=body)
            try:
                serializer.is_valid(raise_exception=True)
                print(serializer)
                # article = Article.objects.create(**serializer.validated_data)
                article = serializer.save()
                return JsonResponse(serializer.data, status=201)
            except ValidationError as e:
                return HttpResponse(e, status=404)
        return JsonResponse({"message": "Error"}, status=404)

    def put(self, request, *args, pk, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.body:
            body = json.loads(request.body)
            serializer = self.serializer_class(data=body, instance=article)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            except ValidationError as e:
                return HttpResponse(e, status=404)
        return JsonResponse({"message": "Error"}, status=404)

