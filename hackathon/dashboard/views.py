from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SavePoint, DangerArea, DangerPoints
from django.core.serializers import serialize
import requests

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
        danger_type = str(data.get("danger_type")).capitalize()

        danger_area = DangerArea.objects.create(name=name, danger_type=danger_type)
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

def dashboard(request):
    latitude = 53.1235
    longitude = 18.0084
    context = {
        'latitude': latitude,
        'longitude': longitude
    }
    return render(request, 'dashboard.html', context)

def post_danger_area(request):
    areas=[]
    for area in DangerArea.objects.all():
        points = DangerPoints.objects.filter(danger_area=area).all()
        areas.append({
            "name": area.name,
            "type": area.danger_type,
            "points": [
                {
                    "latitude": point.latitude,
                    "longitude": point.longitude
                }
                for point in points
            ]
        })
        

    return JsonResponse(areas, safe=False)


def send_save_points(request):
    url = "http://192.168.43.131:5000"  # Target API URL
    data = {
        "title": "sync_save_points",  # Add a title or comment
        "points": list(SavePoint.objects.values('id', 'latitude', 'longitude'))
    }
    
    try:
        response = requests.post(url, json=data, timeout=1)  # Increased timeout
        response.raise_for_status()  # Raises exception for HTTP errors
        print("Data sent successfully:", response.json())  # Print the response if successful
    except requests.exceptions.Timeout:
        print("Timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


    return redirect('dashboard')

def send_danger_area(request):
    url = "http://192.168.43.131:5000"  # Target API URL
    areas = []  # Initialize as a list to hold multiple danger areas
    for area in DangerArea.objects.all():
        points = DangerPoints.objects.filter(danger_area=area).all()
        areas.append({  # Append each area as a new dictionary entry
            "id": area.id,
            "type": area.danger_type,
            "points": [
                {
                    "latitude": point.latitude,
                    "longitude": point.longitude
                }
                for point in points
            ]
        })
    data = {
        "title": "sync_danger_zones",
        "areas": areas  # List of dictionaries, one for each danger area
    }
    try:
        response = requests.post(url, json=data, timeout=1)  # Increased timeout
        response.raise_for_status()  # Raises exception for HTTP errors
        print("Data sent successfully:", response.json())  # Print the response if successful
    except requests.exceptions.Timeout:
        print("Timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    return redirect('dashboard')

        

def post_all_data(request):

    areas=[]
    for area in DangerArea.objects.all():
        points = DangerPoints.objects.filter(danger_area=area).all()
        areas.append({
            "name": area.name,
            "type": area.danger_type,
            "points": [
                {
                    "latitude": point.latitude,
                    "longitude": point.longitude
                }
                for point in points
            ]
        })
    save_points = list(SavePoint.objects.values('name', 'latitude', 'longitude'))
    for point in save_points:
        areas.append(point)
    return JsonResponse(areas, safe=False)

    

    