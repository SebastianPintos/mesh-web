from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the MapView index.")

def want_see(request, node_name):
    response = "The node what you are requesting for is: %s."
    return HttpResponse(response % node_name)

def map(request):

    return render(request, 'mapView/mapView.html')
