from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from mapView.model_to_json import get_json_from_models, get_nodes

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the MapView index.")

def map(request):
	return render(request, 'mapView/mapView.html')

def node_info(request):
	toSend = get_json_from_models(get_nodes())
	return JsonResponse(toSend, safe=False)