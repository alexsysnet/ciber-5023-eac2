from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
	return HttpResponse("Hola, esta es mi primera web Django con la IOC")


