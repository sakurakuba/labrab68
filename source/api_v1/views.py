from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from datetime import datetime
import json
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from webapp.models import Article


# Create your views here.

@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


def echo_view(request):
    print(request.body)
    body = json.loads(request.body)
    print(body.get("test"))
    response_data = {
        "method": request.method,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "body": body
    }
    # response_data_json = json.dumps(response_data)
    # print(response_data_json)
    # response = HttpResponse(response_data_json)
    # response["Content-Type"] = "application/json"
    response = JsonResponse(response_data)
    return response


def articles_view(request):
    if request.method == 'GET':
        articles = Article.objects.values("title", "content")
        # articles = Article.objects.all()
        # articles_data = []
        # for article in articles:
        #     articles_data.append({
        #         "title": article.title,
        #         "content": article.content
        #     })
        # return JsonResponse(articles_data, safe=False)
        return JsonResponse(list(articles), safe=False)
    elif request.method == 'POST':
        body = json.loads(request.body)
        if len(body.get("title")) < 5:
            return JsonResponse({"message": "Error"}, status=404)
        article = Article.objects.create(**body)
        # return JsonResponse({"id": article.pk})
        return JsonResponse({"id": article.pk}, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
