import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from django.views import View
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from webapp.models import Article
from api_v2.serializers import ArticleSerializer

from api_v2.serializers import ArticleModelSerializer


# Create your views here.


class ArticleView(APIView):  # could be used (View)
    # serializer_class = ArticleSerializer # if using serializers.Serializer
    serializer_class = ArticleModelSerializer  # if using serializers.ModelSerializer

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('pk'):
            article = Article.objects.get(id=self.kwargs.get('pk'))
            article_data = self.serializer_class(article).data
            return Response(article_data)
        else:
            articles = Article.objects.all()
            # print(articles)
            # print(self.serializer_class(articles, many=True).data)  # if sending list objects need add many=True
            articles_data = self.serializer_class(articles, many=True).data
            # return JsonResponse(articles_data, safe=False) # without Response lib
            return Response(articles_data)  # with Responses lib

    # this is if we working without Response, using request.body
    # def post(self, request, *args, **kwargs):
    #     if request.body:
    #         body = json.loads(request.body)
    #         serializer = self.serializer_class(data=body)
    #         try:
    #             serializer.is_valid(raise_exception=True)
    #             print(serializer)
    #             # article = Article.objects.create(**serializer.validated_data)
    #             article = serializer.save()
    #             return JsonResponse(serializer.data, status=201)
    #         except ValidationError as e:
    #             return HttpResponse(e, status=404)
    #     return JsonResponse({"message": "Error"}, status=404)



    # this is if we working with Response, use request.data
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


    # this is if we working without Response, using request.body
    # def put(self, request, *args, pk, **kwargs):
    #     article = get_object_or_404(Article, pk=pk)
    #     if request.body:
    #         body = json.loads(request.body)
    #         serializer = self.serializer_class(data=body, instance=article)
    #         try:
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()
    #             return JsonResponse(serializer.data, status=200)
    #         except ValidationError as e:
    #             return HttpResponse(e, status=404)
    #     return JsonResponse({"message": "Error"}, status=404)


    def put(self, request, *args, pk, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, *args, pk, **kwargs):
        Article.objects.get(id=pk).delete()
        return Response(pk)


