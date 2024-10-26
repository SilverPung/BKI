from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SavePoint, DangerArea, DangerPoints
from django.core.serializers import serialize

# Create your views here.


def save_points(request):
    latitude = 53.1235
    longitude = 18.0084
    context = {
        'latitude': latitude,
        'longitude': longitude
    }
    return render(request, 'save_points.html', context)

@csrf_exempt
def get_save_point(request):
    if request.method == "POST":
        
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        name = str(data.get("name")).capitalize()

        save_point = SavePoint.objects.create(latitude=latitude, longitude=longitude, name=name)
        save_point.save()
        

        return JsonResponse({"status": "success", "latitude": latitude, "longitude": longitude, "name": name})
    return JsonResponse({"status": "failed"}, status=400)

def post_save_points(request):
    save_points = SavePoint.objects.values('name', 'latitude', 'longitude')
    return JsonResponse(list(save_points), safe=False)

def danger_area(request):
    latitude = 53.1235
    longitude = 18.0084
    context = {
        'latitude': latitude,
        'longitude': longitude
    }
    return render(request, 'danger_area.html', context)

@csrf_exempt
def get_danger_area(request):
    
    if request.method == "POST":
        
        data = json.loads(request.body)

        print(data)
        
        name = str(data.get("name")).capitalize()
        danger_area = DangerArea.objects.create(name=name)
        danger_area.save()

        points_data = data.get("vertices", [])
        danger_points = []

        for point in points_data:
            latitude = point[0]
            longitude = point[1]
            danger_point = DangerPoints(latitude=latitude, longitude=longitude, danger_area=danger_area)

            danger_points.append(danger_point)

        danger_points.pop()

        if danger_points:
            DangerPoints.objects.bulk_create(danger_points)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

        