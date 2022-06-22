import folium
from django.shortcuts import render
from dashboard.models import Farm

# Create your views here.

def dashboard_map(request):
    
    coordinates = list(Farm.objects.values_list('latitude', 'langitude'))

    country = [-1.9437057, 29.8805778]  #Rwanda
    map =  folium.Map(location=country, zoom_start=8)

    for item in coordinates:
        folium.Marker(item).add_to(map)
    
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)


    map =  map._repr_html_()
    context = {'map': map,}

    return render(request, 'dashboard/index.html', context)