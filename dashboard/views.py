import csv
import folium
from django.core.cache import cache
from django.shortcuts import render
from django.shortcuts import HttpResponse
from dashboard.models import Farm, Farmer
from PIMA_Dashboard.settings import BASE_DIR


START_LOCATION = [0.5050067786194596, 30.879391642411665] # Need to be changed

# Create your views here.
def home(request):

    index = 0
    map = folium.Map(START_LOCATION, zoom_start=5)

    #Training Sessions
    with open(f'{BASE_DIR}/SampleData/TrainingSessions2022.csv') as trainingSessions:
        trainingSessions = csv.reader(trainingSessions, delimiter=',')
        
        for row in trainingSessions:
            if(index==0): 
                index += 1
                continue
        
            if((row[3] == "") or (row[4] == "")): continue

            cord = [float(row[3]), float(row[4])]
            #folium.Marker(cord).add_to(map)
            folium.Marker(
                location=cord,
                tooltip="Training Session",
                icon=folium.Icon(color="blue"),
                ).add_to(map)

    
    #DemoPlot
    index = 0
    with open(f'{BASE_DIR}/SampleData/DemoPlots2022.csv') as demoPlots:
        demoPlots = csv.reader(demoPlots, delimiter=',')

        for row in demoPlots:
            if(index==0): 
                index += 1
                continue
        
            if((row[2] == "") or (row[3] == "")): continue

            cord = [float(row[2]), float(row[3])]
            
            folium.Marker(
                location=cord,
                tooltip="Demo Plot",
                icon=folium.Icon(color="green"),
                ).add_to(map)

    
    #Observation
    observations = cache.get('Observations')

    if observations is not None:

        for obs_ in observations:
            cord = [obs_.get('Observation_Location__Latitude__s'), obs_.get('Observation_Location__Longitude__s')]
            if(cord[0] is None or cord[1] is None): continue
            folium.Marker(
                    location=cord,
                    tooltip="Observation",
                    icon=folium.Icon(color="orange"),
                    ).add_to(map)
    
    
    
    
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.LayerControl().add_to(map)

    map =  map._repr_html_()
    context = {'map': map,}
    return render(request, 'dashboard/index.html', context)


def salesforceObs(request):
    
    observations = cache.get('Observations')

    if observations is None:
        #TODO: Fire background task to fetch data
        return render(request, 'dashboard/salesforce_error.html')
    
    map = folium.Map([observations[0].get('Observation_Location__Latitude__s'), observations[0].get('Observation_Location__Longitude__s')], zoom_start=7)
    for obs_ in observations:
        cord = [obs_.get('Observation_Location__Latitude__s'), obs_.get('Observation_Location__Longitude__s')]
        if(cord[0] is None or cord[1] is None): continue
        folium.Marker(cord, tooltip="Observation").add_to(map)
    
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)


    map =  map._repr_html_()
    context = {'map': map,}

    return render(request, 'dashboard/observations.html', context)


def exported(request):
    #DemoPlots2022.csv
    index = 0
    lat = 0
    lon = 0
    with open(f'{BASE_DIR}/SampleData/DemoPlots2022.csv') as demoPlots:
        demoPlots = csv.reader(demoPlots, delimiter=',')
        for row in demoPlots:
            if(index==0): 
                index += 1
                continue

            if(index==1):
                lat = float(row[2])
                lon = float(row[3])
                index = 0
                break
        map = folium.Map([lat, lon], zoom_start=7)
                
        for row in demoPlots:
            if(index==0): 
                index += 1
                continue
        
            if((row[2] == "") or (row[3] == "")): continue

            cord = [float(row[2]), float(row[3])]
            folium.Marker(cord).add_to(map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.LayerControl().add_to(map)

    map =  map._repr_html_()
    context = {'map': map,}
    return render(request, 'dashboard/test_folium.html', context)



def dummy_map(request):
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

    return render(request, 'dashboard/test_folium.html', context)