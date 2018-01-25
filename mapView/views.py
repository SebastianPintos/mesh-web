from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import mapView.model_to_json as model_to_json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the MapView index.")

def map(request):
	return render(request, 'mapView/mapView.html')

def node_info(request):
	toSend = model_to_json.get_json_from_models(model_to_json.get_nodes())
	return JsonResponse(toSend, safe=False)

def mesh_status(reques):
    toSend = model_to_json.get_json_server_status()
    return JsonResponse(toSend, safe=False)
