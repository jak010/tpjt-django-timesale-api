from django.shortcuts import render

from django.views.generic import View
from django.http.response import JsonResponse


# Create your views here.

class GreetingView(View):

    def get(self, request):
        return JsonResponse(data={
            "Greetings": {
                "title": "This Jako's Template",
                "description": "Hello, Django Users",
            },
            "Author": {
                "Name": "jako",
                "Blog": "https://jakpentest.tistory.com/"
            }
        })
