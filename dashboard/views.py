import csv
import ee
import folium
import datetime
from folium.plugins import MarkerCluster
from django.http import Http404
from django.core.cache import cache
from django.shortcuts import render
from dashboard.models import TrainingSession, DemoPlot, TrainingObservation
from django.template.defaultfilters import slugify
from PIMA_Dashboard.settings import BASE_DIR, env
from .utils import (
    add_basemap_layers,
    add_training_observations,
    add_training_sessions,
    add_demo_plot,
    add_required_objects,
)
from .constant_vars import regions
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required

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

@xframe_options_exempt
@login_required
def index(request):

    #DEFINE: MAP and  Basemaps
    map = folium.Map(START_LOCATION, tiles=None, zoom_start=3)
    add_basemap_layers(map)

    #DEFINE: FEATURE-GROUPS
    featureGroup_training_observation = folium.FeatureGroup(name="Training Observations")
    featureGroup_training_sessions = folium.FeatureGroup(name="Training Sessions")
    featureGroup_demo_plots = folium.FeatureGroup(name="Demo Plots")
    
    #DEFINE: CLUSTERS
    cluster_training_observations = MarkerCluster()
    cluster_training_sessions = MarkerCluster()
    cluster_demo_plots = MarkerCluster()
    

    if request.method == 'GET':

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=90) #3 months ago.

        #QUERY DATA
        TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date])
        TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date])
        Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date])


        #ADD TrainingObservations on MAP
        add_training_observations(map, TrainingObservations, cluster_training_observations, featureGroup_training_observation)

        #ADD Training Sessions on MAP 
        add_training_sessions(map, TrainingSessions, cluster_training_sessions, featureGroup_training_sessions)

        #ADD DemoPlot on MAP
        add_demo_plot(map, Demoplots, cluster_demo_plots, featureGroup_demo_plots)
        

        #ADD: legend && Layer controller
        add_required_objects(map)

        programs = list(cache.get('Programs').values())

        context = {
            'map': map._repr_html_(),
            'programs': programs,
            'regions': regions
        }
        return render(request, 'dashboard/index.html', context)


    if request.method == 'POST':

        #GETTING DATES
        end_date_ = request.POST.get('end-date')
        start_date_ = request.POST.get('start-date')

        if(len(end_date_) == 0): end_date = datetime.date.today()
        else: end_date = datetime.date.fromisoformat(end_date_)

        if (len(start_date_) == 0): start_date = end_date - datetime.timedelta(days=3650) # 10 years ago
        else: start_date = datetime.date.fromisoformat(start_date_)

        #GETTING: programs
        selected_programs = request.POST.getlist('programs')
        
        if (len(selected_programs) == 0):
            TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date])
            TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date])
            Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date])

        else:
            TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)


        #TrainingObservations
        add_training_observations(map, TrainingObservations, cluster_training_observations, featureGroup_training_observation)

        #Training Sessions
        add_training_sessions(map, TrainingSessions, cluster_training_sessions, featureGroup_training_sessions)


        #DemoPlot
        add_demo_plot(map, Demoplots, cluster_demo_plots, featureGroup_demo_plots)

        add_required_objects(map)  

        programs = list(cache.get('Programs').values())
        
        context = {
            'map': map._repr_html_(),
            'programs': programs,
            'regions': regions,
            'selected_programs':selected_programs,
            'start_date': start_date_,
            'end_date': end_date_
        }   
        return render(request, 'dashboard/index.html', context)


@xframe_options_exempt
def project_details(request, slug=None):
    
    #DEFINE: MAP and  Basemaps
    map = folium.Map(START_LOCATION, tiles=None, zoom_start=3)
    add_basemap_layers(map)
    
    
    if slug is not None:
        try:
            Observation_Query =  TrainingObservation.objects.filter(Project_Name_c_slug__iexact=slug)
            Training_session_Query = TrainingSession.objects.filter(Project_Name_c_slug__iexact=slug)
            demo_plot_Query = DemoPlot.objects.filter(Project_Name_c_slug__iexact=slug)
        except:
            raise Http404

        featureGroup_training_observation = folium.FeatureGroup(name="TrainingObservations")
        featureGroup_training_sessions = folium.FeatureGroup(name="Training Sessions")
        featureGroup_demo_plots = folium.FeatureGroup(name="Demo Plots")

        cluster_training_observations = MarkerCluster()
        cluster_training_sessions = MarkerCluster()
        cluster_demo_plots = MarkerCluster()

        #TrainingObservations
        add_training_observations(map, Observation_Query, cluster_training_observations, featureGroup_training_observation)

        #Training Sessions
        add_training_sessions(map, Training_session_Query, cluster_training_sessions, featureGroup_training_sessions)

        #DemoPlot
        add_demo_plot(map, demo_plot_Query, cluster_demo_plots, featureGroup_demo_plots)

    add_required_objects(map)  

    context = {'map': map._repr_html_()}
    return render(request, 'dashboard/project.html', context)

@login_required
def project_list(request):

    projects =  cache.get('Projects')
    projects_ = dict()

    for proj in projects: projects_[proj] = slugify(proj)
    
    context = {'projects': projects_}
    return render(request, 'dashboard/project_list.html', context)
