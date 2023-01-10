from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from menuRecommendation.models import Menu
from menuRecommendation.serializers import MenuSerializer
from menuRecommendation.tasteClassifier import sentence_analyze
from django.views import View
import json

# Create your views here.

def menu_list(request):
    # if request.method == 'GET':
    #     query_set = Menu.objects.all()
    #     serializer = MenuSerializer(query_set, many=True)
    #     sentence = request.GET.get('query', None)
    #     print(sentence)
    #     return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class AnswerView(View):
    def get(self, request):
        sentence = request.GET.get('query', None)
        is_soup = request.GET.get('is_soup', False)
        data = json.loads(request.body)
        except_menus = data['except']
        print(except_menus)
        flavor_weight = sentence_analyze(sentence)

        query_set = Menu.objects.filter(soup = is_soup)
        menu_score = []
        for menu in query_set:
            if menu.name not in except_menus:
                flavor = [menu.spicy, menu.sour, menu.sweet, menu.bitter, menu.salty]
                score = 0
                for i in range(5):
                    score += flavor[i] * flavor_weight[i]
                if score >= 0:
                    temp = (menu.id, score)
                    menu_score.append(temp)

        menu_score.sort(key = lambda x : -x[1])
        result = []
        for i in range(min(10, len(menu_score))):
            temp_id = menu_score[i][0]
            temp_score = menu_score[i][1]
            qs = Menu.objects.filter(id=temp_id)
            temp_name = qs.first().name
            result.append({"name" : temp_name, "score" : temp_score})

        return JsonResponse(result, status = 200, safe = False)

        