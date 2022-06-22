import folium
from django.shortcuts import render
from dashboard.models import Farm, Farmer

# Create your views here.

def dashboard_map(request):
    
    #coordinates = list(Farm.objects.values_list('latitude', 'langitude'))
    farms = list(Farm.objects.values())

    country = [-1.9437057, 29.8805778]  #Rwanda
    map =  folium.Map(location=country, zoom_start=8)

    for item in farms:
        cord = [item.get('latitude'), item.get('langitude')]
        owner = Farmer.objects.get(id=item.get('owner_id')).firstname
        trees = item.get('number_of_trees')
        UPI = item.get('UPI')
        #pop_info = f'Trees:{trees} Trees:{trees}'
        pop_info = f'<i>Owner</i>:<b>{owner}</b><br><i>Trees</i>:<b>{trees}</b><br><i>UPI</i>:<b>{UPI}</b>'
        folium.Marker(cord, popup=pop_info, tooltip = "Click me!").add_to(map)
    
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)


    map =  map._repr_html_()
    context = {'map': map,}

    return render(request, 'dashboard/index.html', context)