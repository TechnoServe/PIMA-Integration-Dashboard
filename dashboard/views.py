import csv
import ee
import folium
import datetime
from django.core.cache import cache
from django.shortcuts import render
from django.shortcuts import HttpResponse
from dashboard.models import Observation_c, Training_Session_c
from PIMA_Dashboard.settings import BASE_DIR, env
from .utils import basemaps
from .legends import macro_en

START_LOCATION = [-0.9019047458079028, 1.093501788502551]

# GCP_credentials = ee.ServiceAccountCredentials(env('GOOGLE_SERVICE_ACCOUNT'), env('PRIVATE_KEY'))
# ee.Initialize(GCP_credentials)

# def add_ee_layer(self, ee_image_object, vis_params, name):
#   map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
#   folium.raster_layers.TileLayer(
#       tiles=map_id_dict['tile_fetcher'].url_format,
#       attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
#       name=name,
#       overlay=True,
#       control=True
#   ).add_to(self)


def index(request):
    
    
    if request.method == 'GET':
        map = folium.Map(START_LOCATION, zoom_start=3)
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=15)

        Observations = Observation_c.objects.filter(Date_c__range=[start_date, end_date])
        TrainingSessions = Training_Session_c.objects.filter(Date_c__range=[start_date, end_date])
        
        feature_group_Observations = folium.FeatureGroup(name="Observations")
        feature_group_training_sessions = folium.FeatureGroup(name="Training Sessions")
        
        #Observations
        for Observation in Observations:
            cord = [Observation.Observation_Location_Latitude_s, Observation.Observation_Location_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue
            
            date_ = Observation.Date_c
            trainer_ = Observation.Trainer_c
            project_ = Observation.Project_Name_c
            participants_ = Observation.Number_of_Participants_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Project</i>:<b>{project_}</b></br><i>Participants</i>:<b>{participants_}</b><br><img src="https://www.technoserve.org/wp-content/uploads/2021/01/CajuLab-photo-1-300x225.png"/>'
            folium.Marker(
                    location=cord,
                    tooltip="Observation",
                    popup = pop_info,
                    icon=folium.Icon(color="red"),
                    ).add_to(feature_group_Observations)
        feature_group_Observations.add_to(map)

        #Training Sessions
        for TrainingSession in TrainingSessions:
            cord = [TrainingSession.Location_GPS_Latitude_s, TrainingSession.Location_GPS_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue

            date_ = TrainingSession.Date_c
            trainer_ = TrainingSession.Trainer_c
            group_ = TrainingSession.Training_Group_c
            module_ = TrainingSession.Module_Name_c
            project_ = TrainingSession.Project_Name_c
            attendance_ = TrainingSession.Number_in_Attendance_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Module</i>:<b>{module_}</b><br><i>Attendance</i>:<b>{attendance_}</b><br><i>Group</i>:<b>{group_}</b><br><i>Project</i>:<b>{project_}</b><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHYRZU5OjdnP0OKZWKIFy1aCnnlqRaVmVre2t3k3BVkVhIXYKLJjFe5Ng1mOXgWfVex2Y&usqp=CAU"/>'
            folium.Marker(
                location=cord,
                tooltip="Training Session",
                popup = pop_info,
                icon= folium.Icon(color="blue"),
                ).add_to(feature_group_training_sessions)
        feature_group_training_sessions.add_to(map)



        #Map Layers
        basemaps['Google Maps'].add_to(map)
        basemaps['Google Satellite'].add_to(map)
        basemaps['Esri Satellite'].add_to(map)

        map.add_child(folium.LayerControl())
        map.add_child(macro_en)

        map =  map._repr_html_()
        programs = cache.get('Programs')
        programs = list(programs.values())
        regions = ['East Africa', 'West Africa', 'Southern Africa', 'India', 'Latino America']
        context = {'map': map, 'programs': programs, 'regions': regions}
        return render(request, 'dashboard/index.html', context)


    if request.method == 'POST':
        map = folium.Map(START_LOCATION, zoom_start=3)

        # print("Requests: ", request.POST)
        # print(list(request.POST.get('end_date')))
        # print(type(list(request.POST.get('end_date'))))
        # print(type(request.POST.get('start_date')))
       


        #Getting Dates
        end_date = request.POST.get('end_date')
        start_date = request.POST.get('start_date')

        if(len(end_date) == 0):
            end_date = datetime.date.today()
        else:
            end_date = datetime.date.fromisoformat(end_date)
            

        if (len(start_date) == 0):
            start_date = end_date - datetime.timedelta(days=530)
        else:
            start_date = datetime.date.fromisoformat(start_date)
            

        #Getting Programs
        selected_programs = request.POST.getlist('programs')
        
        if (len(selected_programs) == 0):
            Observations = Observation_c.objects.filter(Date_c__range=[start_date, end_date])
            TrainingSessions = Training_Session_c.objects.filter(Date_c__range=[start_date, end_date])

        else:
            Observations = Observation_c.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            TrainingSessions = Training_Session_c.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
        
        feature_group_Observations = folium.FeatureGroup(name="Observations")
        feature_group_training_sessions = folium.FeatureGroup(name="Training Sessions")


        #Observations
        for Observation in Observations:
            cord = [Observation.Observation_Location_Latitude_s, Observation.Observation_Location_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue
            
            date_ = Observation.Date_c
            trainer_ = Observation.Trainer_c
            project_ = Observation.Project_Name_c
            participants_ = Observation.Number_of_Participants_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Project</i>:<b>{project_}</b></br><i>Participants</i>:<b>{participants_}</b><br><img src="https://www.technoserve.org/wp-content/uploads/2021/01/CajuLab-photo-1-300x225.png"/>'
            folium.Marker(
                    location=cord,
                    tooltip="Observation",
                    popup = pop_info,
                    icon=folium.Icon(color="red"),
                    ).add_to(feature_group_Observations)
        feature_group_Observations.add_to(map)

        #Training Sessions
        for TrainingSession in TrainingSessions:
            cord = [TrainingSession.Location_GPS_Latitude_s, TrainingSession.Location_GPS_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue

            date_ = TrainingSession.Date_c
            trainer_ = TrainingSession.Trainer_c
            group_ = TrainingSession.Training_Group_c
            module_ = TrainingSession.Module_Name_c
            project_ = TrainingSession.Project_Name_c
            attendance_ = TrainingSession.Number_in_Attendance_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Module</i>:<b>{module_}</b><br><i>Attendance</i>:<b>{attendance_}</b><br><i>Group</i>:<b>{group_}</b><br><i>Project</i>:<b>{project_}</b><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHYRZU5OjdnP0OKZWKIFy1aCnnlqRaVmVre2t3k3BVkVhIXYKLJjFe5Ng1mOXgWfVex2Y&usqp=CAU"/>'
            folium.Marker(
                location=cord,
                tooltip="Training Session",
                popup = pop_info,
                icon= folium.Icon(color="blue"),
                ).add_to(feature_group_training_sessions)
        feature_group_training_sessions.add_to(map)



        #Map Layers
        basemaps['Google Maps'].add_to(map)
        basemaps['Google Satellite'].add_to(map)
        basemaps['Esri Satellite'].add_to(map)

        map.add_child(folium.LayerControl())
        map.add_child(macro_en)

        map =  map._repr_html_()

        programs = cache.get('Programs')
        programs = list(programs.values())
        
        regions = ['East Africa', 'West Africa', 'Southern Africa', 'India', 'Latino America']
        context = {'map': map, 'programs': programs, 'regions': regions}
        return render(request, 'dashboard/index.html', context)

















# def home(request):
#     vis_params = {'min': 0, 'max':4000, 'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
#     map = folium.Map(START_LOCATION, zoom_start=5)
#     #folium.Map.add_ee_layer = add_ee_layer
#     #dem = ee.Image('USGS/SRTMGL1_003')


#     ###############


#     index = 0
#     #Training Sessions
#     feature_group_training_sessions = folium.FeatureGroup(name="Training Sessions")
#     training_icon_url = "https://cdn.mapmarker.io/api/v1/font-awesome/v5/pin?icon=fa-warehouse&size=50&hoffset=0&voffset=-1&background=1167b1"

#     with open(f'{BASE_DIR}/SampleData/TrainingSessions2022.csv') as trainingSessions:
#         trainingSessions = csv.reader(trainingSessions, delimiter=',')
        
#         for row in trainingSessions:
#             if(index==0): 
#                 index += 1
#                 continue
        
#             if((row[3] == "") or (row[4] == "")): continue

#             cord = [float(row[3]), float(row[4])] 
#             pop_info = f'<i>Trainer</i>:<b>{row[10]}</b><br><i>Group</i>:<b>{row[9]}</b><br><i>Project</i>:<b>{row[6]}</b><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHYRZU5OjdnP0OKZWKIFy1aCnnlqRaVmVre2t3k3BVkVhIXYKLJjFe5Ng1mOXgWfVex2Y&usqp=CAU"/>'
#             folium.Marker(
#                 location=cord,
#                 tooltip="Training Session",
#                 popup = pop_info,
#                 icon= folium.Icon(color="blue"),
#                 ).add_to(feature_group_training_sessions)


#     #DemoPlot
#     index = 0
#     feature_group_demoPlots = folium.FeatureGroup(name="Demo Plots")
#     with open(f'{BASE_DIR}/SampleData/DemoPlots2022.csv') as demoPlots:
#         demoPlots = csv.reader(demoPlots, delimiter=',')

#         for row in demoPlots:
#             if(index==0): 
#                 index += 1
#                 continue
        
#             if((row[2] == "") or (row[3] == "")): continue

#             cord = [float(row[2]), float(row[3])]
#             pop_info = f'<i>Observer</i>:<b>{row[8]}</b><br><i>Owner</i>:<b>{row[7]}</b><br><i>Project</i>:<b>{row[5]}</b>'
#             folium.Marker(
#                 location=cord,
#                 tooltip="Demo Plot",
#                 popup = pop_info,
#                 icon=folium.Icon(color="green"),
#                 ).add_to(feature_group_demoPlots)

        
#     #Observation
#     observations = cache.get('Observations')
#     #Programs
#     programs = cache.get('Programs')

#     feature_group_Observations = folium.FeatureGroup(name="Observations")
#     if observations is not None:

        
#         for obs_ in observations:
#             cord = [obs_.get('Observation_Location__Latitude__s'), obs_.get('Observation_Location__Longitude__s')]
#             if(cord[0] is None or cord[1] is None): continue
#             date_ = obs_.get('Date__c')
#             trainer_ = obs_.get('Trainer__c')
#             project_ = obs_.get('Project_Name__c')
#             pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Project</i>:<b>{project_}</b><br><img src="https://www.technoserve.org/wp-content/uploads/2021/01/CajuLab-photo-1-300x225.png"/>'
#             folium.Marker(
#                     location=cord,
#                     tooltip="Observation",
#                     popup = pop_info,
#                     icon=folium.Icon(color="red"),
#                     ).add_to(feature_group_Observations)


#     feature_group_training_sessions.add_to(map)
#     feature_group_demoPlots.add_to(map)
#     feature_group_Observations.add_to(map)

#     #Map Layers
#     basemaps['Google Maps'].add_to(map)
#     basemaps['Google Satellite'].add_to(map)
#     basemaps['Esri Satellite'].add_to(map)
#     basemaps['Google Terrain'].add_to(map)


#     #map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, "TESTNAME")
#     map.add_child(folium.LayerControl())
#     map.add_child(macro_en)

#     map =  map._repr_html_()
#     context = {'map': map, 'programs': programs}
#     return render(request, 'dashboard/index.html', context)
    
