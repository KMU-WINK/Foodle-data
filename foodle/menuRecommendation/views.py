from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from menuRecommendation.models import Menu
from menuRecommendation.serializers import MenuSerializer, BannedMenuSerializer
from menuRecommendation.tasteClassifier import sentence_analyze
from rest_framework.views import APIView 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi      
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

class AnswerView(APIView):

    sentence = openapi.Parameter('sentence', openapi.IN_QUERY, description='사용자가 입력한 문장', required=True, type=openapi.TYPE_STRING)
    is_soup = openapi.Parameter('is_soup', openapi.IN_QUERY, description='국물 여부', required=True, type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], manual_parameters=[sentence, is_soup], request_body=BannedMenuSerializer, responses={200: 'Success'})

    def post(self, request):
        sentence = request.GET.get('sentence', None)
        is_soup = request.GET.get('is_soup', False)
        if is_soup == "true":
            is_soup = True
        else:
            is_soup = False
        data = json.loads(request.body)
        except_menus = data['ban']
        no_nations = data['nation']
        etc = data['etc']
        flavor_weight = sentence_analyze(sentence)

        query_set = Menu.objects.filter(soup = is_soup)
        if len(no_nations) != 0:
            if 0 not in no_nations:
                query_set.exclude(nation = "한식")
            if 1 not in no_nations:
                query_set.exclude(nation = "중식")
            if 2 not in no_nations:
                query_set.exclude(nation = "일식")
            if 3 not in no_nations:
                query_set.exclude(nation = "양식")
        
        if sum(etc) == 1:
            if etc[0]:
                query_set.filter(meat = 1)
            if etc[2]:
                query_set.filter(noodle = 1)
            if etc[1]:
                query_set.filter(rice = 1)
        elif sum(etc) == 2:
            if etc[0] and etc[2]:
                a = query_set.filter(meat = 1)
                b = query_set.filter(noodle = 1)
                query_set = a | b
            if etc[0] and etc[1]:
                a = query_set.filter(meat = 1)
                b = query_set.filter(rice = 1)
                query_set = a | b
            if etc[1] and etc[2]:
                a = query_set.filter(noodle = 1)
                b = query_set.filter(rice = 1)
                query_set = a | b

        elif sum(etc) == 3:
            a = query_set.filter(meat = 1)
            b = query_set.filter(rice = 1)
            c = query_set.filter(noodle = 1)
            query_set = a | b | c

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

        