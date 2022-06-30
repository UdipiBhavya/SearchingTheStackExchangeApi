from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import requests
import re
from ratelimit.decorators import ratelimit
# Create your views here.
def display(request):
    return render(request,'search_questions.html')


@ratelimit(key='ip', rate='5/m',block=True)
@ratelimit(key='ip', rate='100/d',block=True)
def search_questions(request):
    
        
    try:
        string1 = ""
        print(request.POST)
        request_data = json.dumps(request.POST)
        request_data = json.loads(request_data)
        request_data.pop('csrfmiddlewaretoken')
        print(request_data)
        request_data["page"] = request_data.get("page") if request_data['page'] else "1"
        for i in list(request_data):
            print(i)
            if request_data[i] != "" and i !="csrfmiddlewaretoken":
                print(i)
                print("uuu")
                string1+="&"+i+"="+request.POST[i]
                print(string1)
        print(string1)
        if string1 not in request.session.keys():
            print("not")
            site = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&site=stackoverflow"+string1
            print(site)
            r = requests.get(site).content
            request.session[string1] =  json.loads(json.dumps(json.loads(r)))
        # for i in json.loads(json.dumps(json.loads(r)))['items']:
        

        print(request_data['page'])
        return render(request,"search_questions.html",{"questions":request.session[string1],"page":request_data.get('page',1)})
    except ratelimit.exceptions.Ratelimited:
        return HttpResponse('Sorry you are blocked', status=429)
   